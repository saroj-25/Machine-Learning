#import required libraries for flask 

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

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Users(username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cur.close()
            conn.close()
            flash("User Registered Successfully", "success")
            return redirect(url_for('login'))  # Optional: redirect after POST
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("register.html")


@app.route('/login')
def login(): 
    return render_template("login.html")

@app.route('/crack')
def crack(): 
    return render_template("crack.html")

#run flask applicaiton 
if __name__ == '__main__':
    app.run(debug= True)