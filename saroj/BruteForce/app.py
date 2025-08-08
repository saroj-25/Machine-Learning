#import required libraries for flask 

from shlex import quote
from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify

import mysql.connector
import hashlib
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

#mysql connection 
db_config={
    "host" : "localhost", 
    "user" : "root", 
    "password" : "S@r0ji@m17", 
    "database" : "MachineLearning"
}

#password encryption 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        password = hash_password(request.form['password'])
        
        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")
        
        #exception 
        try:
            #insert user into database 
            conn = get_db_connection()
            cur=conn.cursor()
            cur.execute("INSERT INTO Users(UserName,Password)VALUES(%s,%s)",(userName,password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("Registration successful!")
            return redirect(f"/register?msg={msg}")
        except Exception as e: 
            msg = quote(f"Error: {e}")
            return redirect(f"/register?msg={msg}")

    return render_template("register.html",message ="User Registered Sucessfully",category= "success")

@app.route('/login',methods=['GET', 'POST'])
def login(): 
    
   
    if request.method =='POST':
        username = request.form['userName']
        print(f"Debug: {username}")
        
        action = request.form['action'] #login, bruteforce
        print(f"Debug: {username}")
        
        #database connection 
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Password FROM Users WHERE UserName = %s",(username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row: 
            msg = quote("User not found")
            redirect(f"/login?msg={msg}") 
            
        stored_hash = row[0] 
        print(f"Debug: {stored_hash}")
        print(f"Debug: {action}")
        
        if(action == 'login'):
            password = request.form['password']
            if hash_password(password) == stored_hash:
                session['username'] = username
                msg = quote("Logged in Sucessfully !!")
                return redirect(f"/")
            else: 
                msg = quote("Incorrect username or password")
                return redirect(f"/login?msg={msg}")
                
            
        #  elif (action == 'brute'):
            
            
        
    
    return render_template("login.html")

@app.route('/')
def logout():
    return render_template(url_for('home'))

@app.route('/crack',methods=['GET', 'POST'])
def crack(): 
    return render_template("crack.html")

#run flask applicaiton 
if __name__ == '__main__':
    app.run(debug= True)