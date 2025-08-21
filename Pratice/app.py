import pandas as pd
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy 

app=Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db=SQLAlchemy(app)

class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20),nullable=False)
    content=db.Column(db.Text)

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username == 'Mindstix' and password == 'mindstix':
            return "Success"
        else:
            return "Failure"

@app.route("/uploadFile",methods=['POST'])
def uploadFile():
    file=request.files['file']
    if file.content_type == 'text/plain':
        return file.read().decode()
    elif file.content_type == 'application/vnd.ms-excel' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
        return df.to_html()
    elif file.content_type == "text/csv":
        df = pd.read_csv(file)
        return df.to_html()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
