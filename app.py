from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm # pip install flask_wtf
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
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
    form = RegisterForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Pass
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username = form.username.data,
                         email = form.email.data,
                         password_hash = hashed_pw)
            db.session.add(user)
            flash("Registration Successful", "success")
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("Email already registered", "warning")  
        
        
    # conf_users = Users.query.order_by(Users.date_added) 
    return render_template('register.html', form=form)



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

if __name__ == '__main__':
    app.run(debug=True)
