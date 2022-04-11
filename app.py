from flask import Flask, render_template, request, redirect, url_for # pip install flask
from flask_sqlalchemy import SQLAlchemy # pip install flask-sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # this is the path to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this is to prevent warning messages
db = SQLAlchemy(app) # you create the actual database  


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # this is the primary key of the table and so you have a unique value
    title = db.Column(db.String(100)) # this is the title of the todo and has a maximum length of 100 characters
    complete = db.Column(db.Boolean) # this is the boolean value of the todo

@app.route('/') # decorator, this is the route
def index(): #this is for the index page
    todo_list = Todo.query.all() # this is the query to get all the todos
    return render_template('basic.html', todo_list=todo_list) #this is the html file, you have render_template to render the html file

@app.route('/add', methods=['POST']) # this is the route for the add page
def add():
    # add new items to the database
    title = request.form.get('title') # this is the title of the todo
    new_todo = Todo(title=title, complete=False) # this is the new todo
    db.session.add(new_todo) # this is to add the new todo to the database
    db.session.commit() # this is to commit the new todo to the database
    return redirect(url_for('index')) # this is to redirect to the index page


@app.route('/update/<int:todo_id>') # this is the route for the update page
def update(todo_id): # this is the todo that you want to update and you need to pass the todo_id
    # update items in the database
    todo = Todo.query.filter_by(id=todo_id).first() # this is the todo that you want to update
    todo.complete = not todo.complete # this is to toggle the complete value
    db.session.commit() # this is to commit the new todo to the database
    return redirect(url_for('index')) # this is to redirect to the index page


@app.route('/delete/<int:todo_id>') # this is the route for the delete page
def delete(todo_id): # this is the todo that you want to delete and you need to pass the todo_id
    # delete items from the database
    todo = Todo.query.filter_by(id=todo_id).first() # this is the todo that you want to delete
    db.session.delete(todo) # this is to delete the todo from the database
    db.session.commit() # this is to commit the new todo to the database
    return redirect(url_for('index')) # this is to redirect to the index page


if __name__ == '__main__': #this is for the server to run doing it another way
    db.create_all() # this is to create the database
    app.run(debug=True) # just run the app by run following command: python app.py

