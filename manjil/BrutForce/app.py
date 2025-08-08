from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from shlex import quote
import mariadb
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MariaDB connection config
db_config = {
    "host": "localhost",
    "user": "flaskuser",          # <- new user
    "password": "flaskpass",      # <- new password
    "database": "MachineLearning",
    "port": 3306
}

# Password encryption
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        userName = request.form['userName']
        password = request.form['password']
        
        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")
        
        hashed_password = hash_password(password)
        
        try:
            conn = get_db_connection()
            if not conn:
                msg = quote("Database connection error")
                return redirect(f"/register?msg={msg}")
            
            cur = conn.cursor()
            cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (userName, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("User Registered Successfully")
            return redirect(f"/register?msg={msg}")
        except mariadb.Error as e:
            message = quote(f"Error: {e}")
            return redirect(f"/register?msg={message}")
    return render_template("register.html", message="user register successfully")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['password']
        action = request.form.get('action')

        conn = get_db_connection()
        if not conn:
            msg = quote("Database connection error")
            return redirect(f"/login?msg={msg}")
        
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            msg = quote("User not Found") 
            return redirect(f"/login?msg={msg}")

        if action == 'login':
            stored_hash = row[0]
            if hash_password(password) == stored_hash:
                session['username'] = username
                msg = quote("Login successfully!!!")
                return redirect(f"/?msg={msg}")
            else:
                msg = quote("Incorrect username or password!")
                return redirect(f"/login?msg={msg}")    

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/crack', methods=["GET","POST"])
def crack():
    return render_template("crack.html")

if __name__ == '__main__':
    app.run(debug=True)
