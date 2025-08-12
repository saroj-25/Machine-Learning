from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import hashlib
import os
from shlex import quote
from flask import session
import itertools, string


app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "helloworld@123",
    "database": "myproject",
    "auth_plugin":"helloworld@123"
}

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Get DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")

        hashed_password = hash_password(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO USERS (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            cur.close()
            conn.close()

            msg = quote("Registration successful!")
            return redirect(f"/register?msg={msg}")

        except Exception as e:
            msg = quote(f"Error: {str(e)}")
            return redirect(f"/register?msg={msg}")

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    guess_password=None

    if request.method=='POST':
        username= request.form['username']
        action= request.form['action']    #login,brute force
        

        #database connection
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("Select Password from users where username = %s",( username))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            msg= quote("User not Found")
            redirect(f"/login?msg={msg}")


        stored_hash =  row[0]
        if(action=='login'):
            password = request.form['password']
            if hash_password(password)==stored_hash:
                session['username'] = username
                msg = "Logged in Sucessfully!!"
                redirect(f"/login?msg={msg}")
            else:
                 msg = "Incorret Username and Password !!"
                 redirect(f"/login?msg={msg}")



        elif(action=='bruteforce'):
            charset = string.ascii_lowercase
            for combo in itertools.product(charset, repeat=4):
                guess = ''.join(combo)
                if hash_password(guess)==stored_hash:
                    session['username']= username
                    msg=quote("User logged in sucessfully via brute force")
                    return redirect (f"/login?msg={msg}")
                else:
                    msg=quote("Failed to login using Bruteforce")
                    return redirect(f"/login?msg={msg}")    




    return render_template("login.html", guessed_password=guess_password)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect("/")

@app.route('/crack')
def crack():
    if request.method=='POST':
        hash_to_crack=request.form('hash')
        wordlist=request.form['wordlist'].splitlines()

        for word in wordlist:
            if hash_password(word.strip())==hash_to_crack:
                result=f'Password cracked It was: {word.strip()}'
                msg= quote(result)
                break
            else:
                result="password was not avavilable at wordlist"
                msg= quote(result)
        return redirect(f"/crack?msg={msg}")
            


    return render_template("crack.html")


@app.route('/brute',methods=['POST'])
def brute_force():
    data=request.get_json()
    username=data.get('username')
    output=[]


    #get user password hash from db
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute("SELECT Password FROM Users WHERE username = %s",(username,))
    row=cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify(sucess=false,output={'User not Found'})
    
    target_hash=row[0]


    #try all combination for 4 digit numbers
    for i in range(10000):
        guess=str(i).zfill(4)
        output.append(f"Trying : {guess}")
        if(hash_pass{guess}==target_hash):
            session['username']=username
            output.append(f"Password Matched: {guess}")
            return jsonify(sucess=True,output=output)
    output.append("No password matched")

    return jsonify(sucesss=False , output=output)    

if __name__ == '__main__':
    app.run("127.0.0.1:5000",debug=True)
