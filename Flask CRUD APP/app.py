import os
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#__name__ is the speacial Pyhton variable that gets the name of the current module
#Flask uses it to know where to look for the resources like Templates and static files


basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'database.db')

db=SQLAlchemy(app) #Initializing the database


class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),nullable=False)
    description=db.Column(db.Text)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'


@app.route('/')  #This is a decorator that tells Flask which URL should trigger our function.
def index():
    tasks=Task.query.all() #query the Task model to get list of all objects from the database
    return render_template('index.html',tasks=tasks)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        title=request.form['title']
        description=request.form['description']
        new_task=Task(title=title,description=description)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:task_id>',methods=['GET','POST'])
def edit(task_id):
    task=Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title=request.form['title']
        task.description=request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html',task=task)


@app.route('/delete/<int:task_id>',methods=['POST'])
def delete(task_id):
    task=Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)