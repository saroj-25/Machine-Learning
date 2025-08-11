#import required libraries for flask 

from shlex import quote
from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
import itertools, string
import mysql.connector
import hashlib
import os 

app = Flask(__name__)
app.secret_key = os.urandom(24)

#mysql connection 
db_config={
    "host" : "localhost", 
    "user" : "root", 
    "password" : "S@r0ji@m17", 
    "database" : "MachineLearning"
}

#password encryption 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    username = session.get('username') #get user from 
    return render_template("index.html", username=username)

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        password = hash_password(request.form['password'])
        
        if not userName or not password:
            msg = quote("Username or password cannot be empty.")
            return redirect(f"/register?msg={msg}")
        
        #exception 
        try:
            #insert user into database 
            conn = get_db_connection()
            cur=conn.cursor()
            cur.execute("INSERT INTO Users(UserName,Password)VALUES(%s,%s)",(userName,password))
            conn.commit()
            cur.close()
            conn.close()
            msg = quote("Registration successful!")
            return redirect(f"/register?msg={msg}")
        except Exception as e: 
            msg = quote(f"Error: {e}")
            return redirect(f"/register?msg={msg}")

    return render_template("register.html",message ="User Registered Sucessfully",category= "success")

@app.route('/login',methods=['GET', 'POST'])
def login(): 
    guessed_password = None
    if request.method =='POST':
        username = request.form['userName']
        print(f"Debug: {username}")
        
        action = request.form['action'] #login, bruteforce
        print(f"Debug: {username}")
        
        #database connection 
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Password FROM Users WHERE UserName = %s",(username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row: 
            msg = quote("User not found")
            return redirect(f"/login?msg={msg}") 
            
        stored_hash = row[0] 
        print(f"Debug: {stored_hash}")
        print(f"Debug: {action}")
        
        if(action == 'login'):
            password = request.form['password']
            if hash_password(password) == stored_hash:
                session['username'] = username
                msg = quote("Logged in Sucessfully !!")
                return redirect(f"/")
            else: 
                msg = quote("Incorrect username or password")
                return redirect(f"/login?msg={msg}")
                
        elif (action == 'brute'):
            charset = string.ascii_lowercase
            for combo in itertools.product(charset,repeat=4): 
                guess = ''.join(combo)
                if hash_password(guess) == stored_hash: 
                    session['username'] = username
                    msg = quote("User logged in sucessfully via brute force")
                    return redirect(f"/login?msg={msg}")
                else: 
                    msg = quote("Failed to login using Bruteforce ")
                    return redirect(f"/login?msg={msg}")
    
    return render_template("login.html", guessed_password = guessed_password)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect("/")

@app.route('/crack',methods=['GET', 'POST'])
def crack(): 
    
    if request.method == 'POST': 
        hash_to_crack = request.form['hash']
        wordlist = request.form['wordlist'].splitlines()
        
        print(wordlist)
        
        
        for word in wordlist:
            if hash_password(word.strip())== hash_to_crack:
                print(word)
                result = f'Password cracked It was :{word.strip()}'
                msg = quote(result)
                break; 
            
            else: 
                result = "Password not available at wordlist"
                msg = quote(result)
                
        return redirect(f"/crack?msg={msg}")
            
            
    return render_template("crack.html")

# for brute force attack from JS 

@app.route('/brute', methods = ['POST'])
def brute_force(): 
    data = request.get_json()
    username = data.get('username')
    output = []
    
    #get user password hash from db 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT Password FROM Users WHERE username = %s",(username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row: 
        return jsonify(success=false, output =['User not found'])
    
    target_hash = row[0]
    
    
    #try all combinations for 4 digit numbers 
    
    for i in range(10000): 
        guess = str(i).zfill(4)
        output.append(f"Trying : {guess}")
        if(hash_password(guess) == target_hash):
            session['username'] = username
            output.append(f"Password matched :{guess}")
            return jsonify(success = True, output= output)
    output.append("No password matched ")
    
    return jsonify(success=False, output = output)
    


#run flask applicaiton 
if __name__ == '__main__':
    app.run(debug= True)