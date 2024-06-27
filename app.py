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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = "super secret key"


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Forms


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first() # First searchs for username if it exist. ( username is unique )
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull", "success")
                return redirect(url_for('/posts'))     
            else:
                flash("Wrong Password Try Again", "danger")
        else:
            flash("This user does not exist!")
            
    return render_template('index.html', form=form)



# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    school = db.Column(db.String(255))
    department = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    

# Create a Post Form
class PostForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()], widget=TextArea())
    email = StringField("Email", validators=[DataRequired()])
    school = StringField("School", validators=[DataRequired()])
    department = StringField("Department", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/posts')
def posts():
    # Take all the posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)



class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True) # flask db migrate -m "added username", flask db  upgrade
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Do password
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('Password is a not readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class PasswordForm(FlaskForm):
    email = StringField("Enter Email: ", validators=[DataRequired()])
    password_hash = PasswordField("Enter Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords must match!")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     name = None
#     form = UserForm()
    
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user is None:
#             # Hash the password
#             hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2:sha256")
#             user = Users(username = form.username.data,
#                          name=form.name.data,
#                          email=form.email.data,
#                          password_hash=hashed_pw) # instead of password_hash=form.password_hash.data
#             db.session.add(user)
#             db.session.commit()
            
#         name = form.name.data
#         form.name.data = ''
#         form.username.data = ''
#         form.email.data = ''
#         form.password_hash.data = ''
        
#     our_users = Users.query.order_by(Users.date_added)                
#     return render_template("add_user.html", 
#         form=form,
#         name=name,
#         our_users=our_users)
    


if __name__ == '__main__':
    app.run(debug=True)
