#import required libraries for flask
from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
import mysql.connector
import hashlib
import os


app=Flask(__name__)
app.secret_key=os.urandom(24)

#mysql connection
db_config={
      "host":"localhost",
      "user":"root",
      "password":"helloworld@123",
      "database":"myproject"
}
# password encryption
def hash_passsword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        userName= request.form['username']
        password=hash_passsword(request.form['password'])

        #exception
        try:
            #insert user into database
            conn=get_db_connection()
            cur=conn.cursor()
            cur.execute("INSERT INTO USERS(username,password)VALUES(%s%s)",userName,password)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Error:{e}","danger")            
    
    
    return render_template("register.html", message="User Registered Successfully", category="success")

@app.route('/login')
def login():
    return render_template("login.html")

def login():
    return render_template(url_for('home'))
    action=request.form['action']  #it can be for login,register,bruteforce


@app.route('/crack')
def crack():
    return render_template("crack.html")

#run flask application
if __name__=='__main__':
    app.run(debug=True)