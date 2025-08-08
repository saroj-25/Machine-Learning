#import required libraries for flask 

from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify

import mysql.connector
import hashlib
import os 
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = os.urandom(24)

#mysql connection 
db_config={
    "host" : "localhost", 
    "user" : "root", 
    "password" : "rudra123", 
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['UserName'] 
        password = hash_password(request.form['Password'])

        if not username or not password:
            msg = quote("username or password cannot be empty.")
            return redirect(f"/register?msg=(msg)")
        
        #exception
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Users(username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("Registeration successful! Please log in")
            return redirect(f"/login?msg={msg}")
            
            flash("User Registered Successfully", "success")
            return redirect(url_for('login'))  
        except Exception as e:
            msg = quote(f"Error:{e}")
            return redirect(f"/register?msg={msg}")


    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action')

        if not username or not password:
            msg = quote("Username and password required")
            return redirect(f"/login?msg={msg}")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Password FROM Users WHERE username = %s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            msg = quote("User not found")
            return redirect(f"/login?msg={msg}")

        stored_hash = row[0]

        if action == 'login':
            if hash_password(password) == stored_hash:
                session['username'] = username
                msg = quote("Logged in Successfully!!")
                return redirect(f"/login?msg={msg}")
            else:
                msg = quote("Incorrect username or password!!")
                return redirect(f"/login?msg={msg}")

    return render_template("login.html")


@app.route('/crack', methods=['GET', 'POST'])
def crack(): 
    return render_template("crack.html")

#run flask applicaiton 
if __name__ == '__main__':
    app.run(debug= True)
