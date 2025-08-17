# Import required libraries for Flask
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from shlex import quote

import mariadb
import hashlib
import os
import itertools, string

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MariaDB connection configuration
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

# Connect to MariaDB
def get_db_connection():
    try:
        return mariadb.connect(**db_config)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

@app.route('/')
def home():
    username = session.get('username')
    return render_template("index.html", username=username)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        userName = request.form['username']
        password = request.form['password']

        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")

        hashed_password = hash_password(password)

        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Database connection failed.")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (userName, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("User Registered Successfully")
            return redirect(f"/register?msg={msg}")
        except Exception as e:
            msg = quote(f"Error: {e}")
            return redirect(f"/register?msg={msg}")
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    guess_password = None
    if request.method == 'POST':
        username = request.form['username']
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
            msg = quote("User not found")
            return redirect(f"/login?msg={msg}")

        stored_hash = row[0]

        if action == 'login':
            password = request.form['password']
            if hash_password(password) == stored_hash:
                session['username'] = username
                msg = quote("Login successfully!")
                return redirect(f"/?msg={msg}")
            else:
                msg = quote("Incorrect username or password!")
                return redirect(f"/login?msg={msg}")

        elif action == 'brute':
            charset = string.ascii_lowercase
            for combo in itertools.product(charset, repeat=4):
                guess = ''.join(combo)
                if hash_password(guess) == stored_hash:
                    session['username'] = username
                    msg = quote(f"User logged in via brute force. Password: {guess}")
                    return redirect(f"/login?msg={msg}")
            msg = quote("Failed to login using brute force.")
            return redirect(f"/login?msg={msg}")

    return render_template("login.html", guess_password=guess_password)

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route('/crack', methods=["GET", "POST"])
def crack():
    result = None
    if request.method == "POST":
        hash_to_crack = request.form["hash"]
        wordlist = request.form["wordlist"].splitlines()

        for word in wordlist:
            word = word.strip()
            if hash_password(word) == hash_to_crack:
                result = f'Password cracked! It was: {word}'
                break
        else:
            result = "Password not available in wordlist."

    return render_template("crack.html", result=result)

@app.route('/brute',methods=['POST'])
def brute_force():
    data=request.get_json()
    username=data.get('username')
    output=[]

    #get user password hash from db
    conn=get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=%s",(username,))
    row=cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify(sucess=False,output=['user not found'])
    target_hash=row[0]
    

    # try all combination for 4 digit number
    for i in range(10000):
        guess=str(i).zfill(4)
        output.append(f"Trying: {guess}")
        if(hash_password(guess)==target_hash):
            session['username']=username
            output.append(f"password matched :{guess}")
            return jsonify(success=True,output=output)
    output.append("no password matched")
    return jsonify (success=Flask,output=output)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
