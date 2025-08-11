from flask import Flask, render_template, request, redirect, url_for, flash, session
import itertools, string
import mysql.connector
import hashlib
import os
from urllib.parse import quote
from flask import jsonify


app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "rudra123",
    "database": "MachineLearning"
}

# Password encryption
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    username = session.get('username')  
    return render_template("index.html", username=username)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['UserName']
        password = request.form['Password']

        if not username or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")

        hashed_pw = hash_password(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO Users(username, password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            cur.close()
            conn.close()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            msg = quote(f"Error: {e}")
            return redirect(f"/register?msg={msg}")

    return render_template("register.html")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    guessed_password = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action')

        if not username or not password:
            msg = quote("Username and password required")
            return redirect(f"/login?msg={msg}")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM Users WHERE username = %s", (username,))
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
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
            else:
                msg = quote("Incorrect username or password")
                return redirect(f"/login?msg={msg}")

        elif action == 'brute':
            charset = string.ascii_lowercase
            for combo in itertools.product(charset, repeat=4):
                guess = ''.join(combo)
                if hash_password(guess) == stored_hash:
                    session['username'] = username
                    guessed_password = guess
                    flash(f"Brute-force success! Password is: {guess}", "success")
                    return redirect(url_for('home'))

            msg = quote("Failed to login using brute-force")
            return redirect(f"/login?msg={msg}")

    return render_template("login.html", guessed_password=guessed_password)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/")
# Crack route (placeholder)
@app.route('/crack', methods=['GET', 'POST'])
def crack():
    result = None

    if request.method == 'POST':
        hash_to_crack = request.form['hash']
        wordlist = request.form['wordlist'].splitlines()

        for word in wordlist:
            if hash_password(word.strip()) == hash_to_crack:
                result = f'Password cracked! It was: {word.strip()}'
                msg = quote(result)
                break
        else:
            result = "Password not available in wordlist"
            msg = quote(result)
    return render_template("crack.html", result=result)




@app.route('/brute', methods=['POST'])
def brute_force():
    data = request.get_json()
    username = data.get('username')
    output = []

    conn = get_db_connection()
    cur = conn.cursor()

    
    cur.execute("SELECT password FROM Users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify(success=False, output=['User not found'])

    target_hash = row[0]

    for i in range(10000):
        guess = str(i).zfill(4)
        output.append(f"Trying: {guess}")
        if hash_password(guess) == target_hash:
            session['username'] = username
            output.append(f"Password matched: {guess}")
            return jsonify(success=True, output=output)

    output.append("No password matched")
    return jsonify(success=False, output=output)






# Run Flask app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
