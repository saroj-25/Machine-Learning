#import required libraries fro flask

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

import mysql.connector
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


#mysql connection 
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  
    "database": "machinelearning"
}
#password Encryption

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register' ,methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        userName = request.form['username']
        password = hash_password(request.form['password'])
        # exception
        try:
            #insert user into database
            conn = get_db_connection()
            cur:conn.cursor()
            cur.execute("INSRET INTO Users(username,password)VALUES(%s,%s)",(userName,password))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Error:{e}","danger")
            
          #password
        
    return render_template("register.html",message="User Registered Successfully", category = "success")

@app.route('/login', methods= ['GET','POST'])
def login():
    # action = request.form['action']# action , register, bruteforce.
        
    return render_template("login.html")

@app.route('/')
def logout():
    return render_template(url_for('home'))

@app.route('/crack')
def crack():
    return render_template("crack.html")

#run flask application

if __name__ == '__main__':
    app.run(debug=True)