# flask libraries, render_template for rendering html files, request for finding method types(GET,POST)
from flask import Flask,render_template,request,url_for,redirect 
# postgres driver library
import psycopg2
# for loading the variable in .env file
from dotenv import load_dotenv
# for using file handing or os functionalities
import os
import pandas as pd

#Creating the flask app
app=Flask(__name__)

#function for connecting to the postgres database
def get_db_connection():
    load_dotenv()
    user=os.getenv('DB_USERNAME')
    password=os.getenv('DB_PASSWORD')
    conn=psycopg2.connect(host='localhost',database='flask_ingestion_dashboard_db',user=user,password=password)
    return conn

# route for home/index page
@app.route("/")
def index():
    return render_template('index.html')

# route for upload
@app.route("/upload",methods=['POST'])
def upload():
    if request.method=='POST':
        file=request.form.get('uploads')
        df=pd.read_csv(file)
        print(file)
    return "Uploading in progess"



# main function
if __name__=='__main__':
    app.run(debug=True)
