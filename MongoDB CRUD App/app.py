import os
from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv() #load enviornment variable from .env file

app=Flask(__name__)

#mongoDB connection
MONGO_URI=os.getenv('MONGO_URI')
client=MongoClient(MONGO_URI)

#selecting the database and collection 
# if not present it will create it
db=client.todo_db
tasks_collection=db.tasks

@app.route('/')
def index():
    tasks=tasks_collection.find({})
    return render_template('index.html',tasks=tasks)


@app.route('/add',methods=['POST'])
def add():
    description=request.form['description']
    priority=request.form['priority']
    tasks_collection.insert_one({'description':description,'priority':priority,'status':'Pending'})    
    return redirect(url_for('index'))


@app.route('/delete/<task_id>',methods=['POST'])
def delete(task_id):
    task_id_obj=ObjectId(task_id)
    tasks_collection.delete_one({'_id':task_id_obj})
    return redirect(url_for('index'))

@app.route('/edit/<task_id>',methods=['POST'])
def edit(task_id):
    task_id_obj=ObjectId(task_id)
    description=request.form['description']
    tasks_collection.update_one({'_id':task_id_obj},{'$set':{'description':description}})
    return redirect(url_for('index'))

@app.route('/complete/<task_id>',methods=['POST'])
def complete(task_id):
    task_id_obj=ObjectId(task_id)
    tasks_collection.update_one({'_id':task_id_obj},{'$set':{'status':'completed'}})
    return redirect(url_for('index'))

#running the application
if __name__=='__main__':
    app.run(debug=True)

