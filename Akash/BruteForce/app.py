#import required libraries for flask
import itertools,string
from shlex import quote
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
    username = session.get('username')
    return render_template("index.html", username=username)

@app.route('/register' ,methods=['GET','POST'])
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        password = hash_passsword(request.form['password'])
        
        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")

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
            msg= quote("Registration Successfully")
            return redirect(f"/login?msg={msg}")
        except Exception as e:
            msg= quote(f"Registration failed {e}")
            return redirect(f"/register?msg={msg}")
            
    return render_template("register.html", message="User registered Successfully" , category="success")



@app.route('/login',methods=['GET','POST'])
def login():
    # action = request.form['action']
    guess_Password =None
    if request.method=='POST':
        username= request.form['userName']
        action= request.form['action']

        #database connection 
        conn= get_connection()
        cur = conn.cursor(buffered=True)

        # cur=conn.cursor()
        cur.execute("SELECT password FROM users WHERE Username=%s",(username,))
        # row = cur.fetchall()
        row =cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            msg = quote("User not found")
            return redirect(f"/login?msg={msg}")
        
        stored_hash =row[0]
        print(f"Debug: {stored_hash}")

        if (action == 'login'):

            password = request.form['password']
            
            if hash_passsword(password) == stored_hash:
                session['username']=username
                return redirect("/")
            else:
                msg=quote("Incorrect username or password")
                return redirect(f"/login?msg={msg}")
        elif (action == 'brute'):
            charset = string.ascii_lowercase
            for combo in itertools.product(charset,repeat=4):
                guess = ''.join(combo)
                if hash_passsword(guess) == stored_hash:
                    session['username'] = username
                    msg= quote("User logged in successfully via brute force ")
                    return redirect(f"/login?msg={msg}")
                else:
                    msg =quote("Failed to login using BruteForce ")
                    return redirect(f"/login?msg={msg}")
    return render_template("login.html",guess_Password=guess_Password)

@app.route('/logout')
def logOut():
    session.pop('userName',None)
    return redirect(f'/')

@app.route('/crack',methods=['GET','POST'])
def crack():
    if request.method == 'POST':
        hash_to_crack = request.form['hash']
        wordList = request.form['wordlist'].splitlines()

        print(wordList)

        for word in wordList:
            if hash_passsword (word.strip())==hash_to_crack:
                result =f'PassWord cracked: It was :{word.strip()}'
                msg = quote(result)

                break
            else:
                result="Password not available at wordList"
                msg = quote(result)
        return redirect(f"/crack?msg={msg}")

    return render_template("crack.html")


#for brute force attack from js
@app.route('/brute',methods=['POST'])
def brute_force():
    data= request.get_json()
    username = data.get('username ')
    output =[]


    #get user password hash from db
    conn=get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Password FROM Users WHERE username = %s",(username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify(success=False,output=['User not found'])
    
    target_hash = row[0]


    #try all combinations for 4 digit number

    for i in range(10000):
        guess = str(i).zfill(4)
        output.append(f"Trying:{guess}")
        if(hash_passsword(guess)== target_hash):
            session['username']=username
            output.append(f"Password matched:{guess}")
            return jsonify(success = True, output= output)
    output.append("No password matched")

    return jsonify(success = False, output= output)


@app.route('/',methods=['GET','POST'])
def logout():
        return render_template(url_for('home'))


#run flask application
if __name__=='__main__':
    app.run(debug=True)

