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
      "password":"Cityp@lp@123",
      "database":"MachineLearning"
}

#check database connectivity 


# password encryption
def hash_passsword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        password = hash_passsword(request.form['password'])

         #exception handling
        try:
            conn=get_connection()
            cur=conn.cursor()
            # cur.execute("SHOW DATABASES")
            # conn.commit()
            cur.execute("INSERT INTO Users(userName,password)VALUES(%s,%s)",(userName,password))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Error:{e}","danger")
            
    return render_template("register.html", message="User registered Successfully" , category="success")



@app.route('/login',methods=['GET','POST'])
def login():
    action = request.form['action']

    return render_template("login.html")

@app.route('/crack',methods=['GET','POST'])
def crack():
    return render_template("crack.html")
@app.route('/',methods=['GET','POST'])
def logout():
        return render_template(url_for('home'))


#run flask application
if __name__=='__main__':
    app.run(debug=True)

