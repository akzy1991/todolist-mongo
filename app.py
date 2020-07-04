from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

DB_NAME = 'todolist'


@app.route('/')
def home():
    return "welcome home"


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
    })

    return 'task created'


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
