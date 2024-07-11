import os
import time
import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import RegisterForm, PasswordForm, UserForm, LoginForm, ParticipantForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_restful import Resource, Api
from authlib.integrations.flask_client import OAuth

# dotenv setup
load_dotenv()

# Creating flask instance
app = Flask(__name__)
api = Api(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql1234@db:3306/conf_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Retry mechanism
MAX_RETRIES = 5
for _ in range(MAX_RETRIES):
    try:
        # Initialize the database connection
        db = SQLAlchemy(app)
        break
    except pymysql.err.OperationalError as e:
        print(f"Database connection failed: {e}")
        time.sleep(5)
else:
    print("Could not connect to the database. Exiting.")
    exit(1)

migrate = Migrate(app, db)

# Flask Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# OAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

# Models
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(255))

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

class SchoolList(db.Model):
    __tablename__ = 'school_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return self.school

class DepartmentList(db.Model):
    __tablename__ = 'department_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department = db.Column(db.String(500), nullable=False, unique=True)

    def __repr__(self):
        return self.department

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school_list.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department_list.id'), nullable=False)

    school = db.relationship('SchoolList', backref='participants')
    department = db.relationship('DepartmentList', backref='participants')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry You Must Be The Admin To Access This Page.")
        return redirect(url_for('index'))

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
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        except:
            db.session.rollback()
            flash("Error! ...try again")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)

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
            return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!!")
    return redirect(url_for('login'))

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
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
            user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful", "success")
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/admin/participant_list', methods=['GET', 'POST'])
def part_list():
    participants = db.session.query(Participant).join(SchoolList, Participant.school_id == SchoolList.id).join(DepartmentList, Participant.department_id == DepartmentList.id).all()
    return render_template('part_list.html', users=participants)

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = ParticipantForm()
    schools = db.session.query(SchoolList).all()
    departments = db.session.query(DepartmentList).all()
    form.school.choices = [(school.id, school.school) for school in schools]
    form.department.choices = [(department.id, department.department) for department in departments]

    if form.validate_on_submit():
        new_user = Participant(name=form.name.data, surname=form.surname.data, email=form.email.data, phone=form.phone.data, school_id=form.school.data, department_id=form.department.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('part_list'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = Participant.query.get_or_404(id)
    user.department = DepartmentList.query.get(user.department_id)
    form = ParticipantForm(obj=user)
    schools = SchoolList.query.all()
    departments = DepartmentList.query.all()
    form.school.choices = [(school.id, school.school) for school in schools]
    form.department.choices = [(department.id, department.department) for department in departments]

    if request.method == 'GET':
        form.school.data = user.school_id
        form.department.data = user.department_id

    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.school_id = form.school.data
        user.department_id = form.department.data
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('part_list'))
    return render_template('edit.html', form=form, user=user)

@app.route('/delete/<int:id>')
def delete(id):
    user = Participant.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("Participant Deleted Successfully")
    return redirect(url_for('part_list'))

@app.route('/delete/user/<int:id>')
def delUser(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User Deleted Successfully")
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Google OAuth Routes
@app.route('/google_login')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_login_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/google_register')
def google_register():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_register_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/google_login_authorize')
def google_login_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    user = Users.query.filter_by(email=user_info['email']).first()
    if user is None:
        flash("No account found. Please register first.", "warning")
        return redirect(url_for('register'))
    login_user(user)
    session['profile'] = user_info
    session.permanent = True
    flash("Login successful.", "success")
    return redirect(url_for('dashboard'))

@app.route('/google_register_authorize')
def google_register_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    user = Users.query.filter_by(email=user_info['email']).first()
    if user is not None:
        flash("Account already exists. Please log in.", "warning")
        return redirect(url_for('login'))
    user = Users(username=user_info['email'], email=user_info['email'], password_hash="googleUser")
    db.session.add(user)
    db.session.commit()
    login_user(user)
    session['profile'] = user_info
    session.permanent = True
    flash("Registration successful.", "success")
    return redirect(url_for('dashboard'))


# RESTful API Resources for Users
class UserResource(Resource):
    def get(self, user_id):
        user = Users.query.get_or_404(user_id)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_added': user.date_added.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def put(self, user_id):
        user = Users.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = data['password']
        db.session.commit()
        return {
            'message': 'User updated successfully'
        }
    
    def delete(self, user_id):
        user = Users.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            'message': 'User deleted successfully'
        }

class UserListResource(Resource):
    def get(self):
        users = Users.query.all()
        return [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_added': user.date_added.strftime('%Y-%m-%d %H:%M:%S')
            } for user in users
        ]
    
    def post(self):
        data = request.get_json()
        hashed_pw = generate_password_hash(data['password'], "pbkdf2:sha256")
        new_user = Users(username=data['username'], email=data['email'], password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return {
            'message': 'User created successfully'
        }, 201

# RESTful API Resources for Participants
class ParticipantResource(Resource):
    def get(self, participant_id):
        participant = Participant.query.get_or_404(participant_id)
        return {
            'id': participant.id,
            'name': participant.name,
            'surname': participant.surname,
            'email': participant.email,
            'phone': participant.phone,
            'school_id': participant.school_id,
            'department_id': participant.department_id
        }

    def put(self, participant_id):
        participant = Participant.query.get_or_404(participant_id)
        data = request.get_json()
        participant.name = data.get('name', participant.name)
        participant.surname = data.get('surname', participant.surname)
        participant.email = data.get('email', participant.email)
        participant.phone = data.get('phone', participant.phone)
        participant.school_id = data.get('school_id', participant.school_id)
        participant.department_id = data.get('department_id', participant.department_id)
        db.session.commit()
        return {
            'message': 'Participant updated successfully'
        }

    def delete(self, participant_id):
        participant = Participant.query.get_or_404(participant_id)
        db.session.delete(participant)
        db.session.commit()
        return {
            'message': 'Participant deleted successfully'
        }

class ParticipantListResource(Resource):
    def get(self):
        participants = Participant.query.all()
        return [
            {
                'id': participant.id,
                'name': participant.name,
                'surname': participant.surname,
                'email': participant.email,
                'phone': participant.phone,
                'school_id': participant.school_id,
                'department_id': participant.department_id
            } for participant in participants
        ]
    
    def post(self):
        data = request.get_json()
        new_participant = Participant(
            name=data['name'],
            surname=data['surname'],
            email=data['email'],
            phone=data['phone'],
            school_id=data['school_id'],
            department_id=data['department_id']
        )
        db.session.add(new_participant)
        db.session.commit()
        return {
            'message': 'Participant created successfully'
        }, 201

# Register API Resources
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserListResource, '/api/users')
api.add_resource(ParticipantResource, '/api/participant/<int:participant_id>')
api.add_resource(ParticipantListResource, '/api/participants')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
