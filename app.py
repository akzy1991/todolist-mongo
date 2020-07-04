from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from dotenv import load_dotenv
from bson import ObjectId
import datetime
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

DB_NAME = 'todolist'

SESSION_KEY = os.environ.get('SESSION_KEY')

app.secret_key = SESSION_KEY


@app.route('/')
def home():
    tasks = client[DB_NAME].todos.find()
    return render_template('home.template.html', tasks=tasks)


@app.route('/tasks/create')
def show_create_form():
    return render_template('create_task.template.html')


@app.route('/tasks/create', methods=["POST"])
def process_create_task():
    task_name = request.form.get('task-name')
    due_date = request.form.get('due-date')
    comments = request.form.get('comments')

    client[DB_NAME].todos.insert_one({
        'task_name': task_name,
        'due_date': datetime.datetime.strptime(due_date, '%Y-%m-%d'),
        'comments': comments,
        'done': False
    })

    flash(f'New Task "{task_name}" has been created')
    return redirect(url_for('home'))


@app.route('/tasks/check', methods=['PATCH'])
def check_task():
    task_id = request.json.get('task_id')
    task = client[DB_NAME].todos.find_one({
        "_id": ObjectId(task_id)
    })

    if task.get('done') is None:
        task['done'] = False

    client[DB_NAME].todos.update({
        "_id": ObjectId(task_id)
    }, {
        '$set': {
            'done': not task['done']
        }
    })

    return {
        "status": "OK"
    }


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
