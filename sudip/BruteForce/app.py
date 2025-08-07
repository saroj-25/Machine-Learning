# import  required libraris for Flask

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

import mysql.connector
import hashlib
import os

app = Flask(__name__)
app.secret_key= os.urandom(24)

#mysql configuration (connection)

db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "",
    "database" : "machinelearning"
}

#password encrypt
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_conection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route ('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/crack')
def crack():
    return render_template("crack.html")


#run application

if __name__ == '__main__':
    app.run(debug= True)