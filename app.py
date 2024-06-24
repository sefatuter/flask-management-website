from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
