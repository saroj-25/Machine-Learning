# # import  required libraris for Flask

# from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

# import mysql.connector
# import hashlib
# import os

# app = Flask(__name__)
# app.secret_key= os.urandom(24)

# #mysql configuration (connection)

# db_config = {
#     "host" : "localhost",
#     "user" : "root",
#     "password" : "",
#     "database" : "machinelearning"
# }

# #password encrypt
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def get_db_conection():
#     return mysql.connector.connect(**db_config)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route ('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         UserName = request.form['userName']
#         hash_password = hash_password(request.form['password'])

#         #exception
#         try:
#             #insert userinto database
#             conn = get_db_conection()
#             cur=conn.cursor()
#             cur.execute("INSERT INTO Users (username,password) VALUES(%s,%s)", (UserName,hash_password))
#             conn.commit()
#             cur.close()
#             conn.close()
#         except Exception as e:
#             flash(f"Error: {e}","danger")
        
#         #password

        
#     return render_template("register.html", message= "You Registered!!!", category ="success" )

# @app.route('/login')
# def login():
#     #action = request.form['action'] #used for the login,register,bruteforce

#     return render_template("login.html")

# @app.route('/')
# def logout():
#     return render_template('home')


# @app.route('/crack')
# def crack():
#     return render_template("crack.html")


# #run application

# if __name__ == '__main__':
#     app.run(debug= True)


from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "machinelearning"
}

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    return render_template("index.html")

# Register route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']
        hashed_pw = hash_password(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
            if cur.fetchone():
                flash("Username already exists.", "warning")
            else:
                cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, hashed_pw))
                conn.commit()
                flash("You Registered Successfully!", "success")
                return redirect(url_for('login'))
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("register.html")

# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']
        hashed_pw = hash_password(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, hashed_pw))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template("login.html")

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# Crack route
@app.route('/crack')
def crack():
    return render_template("crack.html")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
