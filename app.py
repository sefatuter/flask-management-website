from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm # pip install flask_wtf
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user # pip install flask_login

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from wtforms.widgets import TextArea
#Creating flask instance
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql1234@localhost/conf_users'
# Secret Key
app.config['SECRET_KEY'] = "super secret key"


db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def index():
    return render_template('index.html')

# Admin Page

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry You Must Be The Admin To Access This Page.")
        return redirect(url_for('index'))

# Dashboard Page

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    
    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        
        try:
            db.session.commit()
            flash("User Updated Successfully!")

            return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("Error! ...try again")
            return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)
    else:
        return render_template("dashboard.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)

# Update Page
@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if id != current_user.id:
        flash("You Can't Edit This User", "danger")
        return redirect(url_for('dashboard'))  # Redirect to dashboard or any appropriate page

    if request.method == "POST":
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        
        try:
            db.session.commit()
            flash("User Updated Successfully!", "success")

            return redirect(url_for('dashboard'))  # Redirect to avoid re-posting the form on refresh
        except:
            db.session.rollback()
            flash("Error! ...try again", "danger")
            return render_template("update.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update=name_to_update,
                id=id)


# Flask Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Login Page

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first() # First searchs for username if it exist. ( username is unique )
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull", "success")
                return redirect(url_for('index'))     
            else:
                flash("Wrong Password Try Again", "danger")
        else:
            flash("This user does not exist!")
          
    return render_template('login.html', form=form)


# Logout Page

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!!")
    return redirect(url_for('login'))


# Register Page

@app.route('/user/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered and logged in.", "info")
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_by_email = Users.query.filter_by(email=form.email.data).first()
        user_by_username = Users.query.filter_by(username=form.username.data).first()
        if user_by_email:
            flash("Email already registered", "warning")
        elif user_by_username:
            flash("Username already taken", "warning")
        else:
            # Hash Pass
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username=form.username.data,
                         email=form.email.data,
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful", "success")
            return redirect(url_for('login'))
        
    # conf_users = Users.query.order_by(Users.date_added) 
    return render_template('register.html', form=form)


# Main Conference Page

@app.route('/admin/participant_list', methods=['GET', 'POST'])
def part_list():
    users = Participant.query.all()
    return render_template('part_list.html', users=users)


@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = ParticipantForm()
    
    # Querying distinct schools and departments from the database
    schools = db.session.query(SchoolList.school).distinct().all()
    departments = db.session.query(DepartmentList.department).distinct().all()

    # Setting choices for the SelectFields
    form.school.choices = [(school[0], school[0]) for school in schools]
    form.department.choices = [(department[0], department[0]) for department in departments]
    
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        phone = form.phone.data
        school = form.school.data
        department = form.department.data
        new_user = Participant(name=name, surname=surname, email=email, phone=phone, school=school, department=department)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('part_list'))
    
    return render_template('add.html', form=form)


class SchoolUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<SchoolUser {self.school} - {self.department}>'
    

# Edit Participant Page
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = Participant.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.school = request.form['school']
        user.department = request.form['department']
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('part_list'))
    return render_template('edit.html', user=user)


# Delete Participant Page
@app.route('/delete/<int:id>')
def delete(id):
    user = Participant.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User Deleted Successfully")
    return redirect(url_for('part_list'))


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)


class ParticipantForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    school = SelectField("School", validators=[DataRequired()], choices=[])
    department = SelectField("Department", validators=[DataRequired()], choices=[])
    submit = SubmitField("Add Participant")



class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False, unique=True) # flask db migrate -m "added username", flask db  upgrade
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128)) # Do Password
    
    
    @property
    def password(self):
        raise AttributeError('Password is a not readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords must match!")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Enter Email: ", validators=[DataRequired()])
    password_hash = PasswordField("Enter Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords must match!")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    
class SchoolList(db.Model):
    __tablename__ = 'school_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return f'<SchoolList {self.name}>'

class DepartmentList(db.Model):
    __tablename__ = 'department_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return f'<DepartmentList {self.name}>'


    
# Create Custom Error Pages

#1-Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#2-Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)
