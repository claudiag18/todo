from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)

# Variables and Constants
x = date.today()
LIST_TITLE = [x.strftime("%A"), x.strftime("%b %d %Y")]


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ToDoList TABLE Configuration
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(250))
    doing_item = db.Column(db.String(250))
    done_item = db.Column(db.String(250))


@app.route('/')
def home():
    list_to_do = db.session.query(Todo).all()
    ToDo_list = []
    for item in list_to_do:
        list_dict = {
            'id': item.id,
            'todo_item': item.todo_item,
            'doing_item': item.doing_item,
            'done_item': item.done_item,
        }
        ToDo_list.append(list_dict)
    return render_template('index.html', list_title=LIST_TITLE, lista=ToDo_list)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        if request.form.get('userInput'):
            new_item = Todo(
                todo_item=request.form.get('userInput'),
                doing_item=None,
                done_item=None,
            )
            db.session.add(new_item)
            db.session.commit()
    return redirect(url_for('home'))


@app.route('/doing/<int:item_id>', methods=['POST'])
def doing(item_id):
    if request.method == 'POST':
        item_to_update = Todo.query.get(item_id)
        item_to_update.doing_item = item_to_update.todo_item
        item_to_update.todo_item = None
        item_to_update.done_item = None
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/done/<int:item_id>', methods=['POST'])
def done(item_id):
    if request.method == 'POST':
        item_to_update = Todo.query.get(item_id)
        item_to_update.done_item = item_to_update.doing_item
        item_to_update.todo_item = None
        item_to_update.doing_item = None
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:item_id>')
def delete(item_id):
    item_to_delete = Todo.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)