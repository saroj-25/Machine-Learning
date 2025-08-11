#Import required libraries for flask

from flask import Flask, render_template, request, redirect, url_for, session, jsonify,flash
from shlex import quote

import mysql.connector
import hashlib
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


# mysql connection
db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "",
    "database" : "MachineLearning"
}


#password encrpytion
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

# @app.route('/register', methods=["GET","POST"])
# def register():
#     if request.method == "POST":
#         userName = request.form['userName']
#         print(userName)
#         password = request.form['password']
#         password = hash_password(password)

#         #exception
#         try:
#             #insert user into database
#             conn = get_db_connection()
#             print("connection check"+conn)
#             cur = conn.cursor()
#             print("Curser check"+cur)
#             cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)",(userName,password))
#             conn.commit()
#             cur.close()
#             conn.close()
#         except Exception as e:
#             flash(f"Error:{e}", "danger")

#     return render_template("register.html", message="User Registered Successfully", category="success")


@app.route('/register', methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        userName = request.form['userName']
        password = request.form['password']
        password = hash_password(password)
        
        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")



        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Users(username, password) VALUES (%s, %s)", (userName, password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("User Registered Successfully")
            return redirect(f"/register?msg={msg}")
        except Exception as e:
            message = quote(f"Error: {e}")
            return redirect(f"/register?msg={message}")
    return render_template("register.html", message="user register sucessfully")



@app.route('/login', methods=["GET","POST"])
def login():
    action = request.form.get('action')   # For login, bruteforce
    
    if request.method == 'POST':
        username = request.form['UserName']


        # database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE UserName = %s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            msg = quote("User not Found") 
            redirect(f"/login?msg={msg}")
            

        if(action == 'login'):
                stored_hash = row[0]
                password = request.form['password']
                if hash_password(password) == stored_hash:
                    session['username'] = username
                    msg = quote("login sucessfully!!!")
                    return redirect(f"/")
                else:
                    msg = quote("Incorrect username or password!")
                    return redirect(f"/login?msg={msg}")    
            
            
            # elif(action == 'brute'):



    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template(url_for('home'))

@app.route('/crack', methods=["GET","POST"])
def crack():
    return render_template("crack.html")


# run flask application
if __name__ == '__main__':
    app.run(debug=True)