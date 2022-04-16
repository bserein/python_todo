from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False) 
    complete = db.Column(db.Boolean) 
    # due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/todo') 
def index(): 
    todo_list = Todo.query.all() 
    return render_template('basic.html', todo_list=todo_list) 

@app.route('/todo/add', methods=['POST']) 
def add():
    
    title = request.form.get('title') 
    # title_due_date = request.form['due_date']
    # datetime_object = datetime.fromisoformat(title_due_date)
    # print(datetime_object)
    # new_todo = Todo(title=title, due_date=datetime_object, complete=False)
    new_todo = Todo(title=title, complete=False) 
    db.session.add(new_todo) 
    db.session.commit() 
    return redirect(url_for('index')) 


@app.route('/todo/update/<int:todo_id>') 
def update(todo_id): 
    todo = Todo.query.filter_by(id=todo_id).first() 
    todo.complete = not todo.complete 
    db.session.commit() 
    return redirect(url_for('index')) 


@app.route('/todo/delete/<int:todo_id>') 
def delete(todo_id): 
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo) 
    db.session.commit() 
    return redirect(url_for('index')) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def signup():
    return render_template('signup.html')


if __name__ == '__main__': 
    db.create_all() 
    app.run(debug=True) 

