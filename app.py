import os
from flask import Flask, render_template, url_for, request, redirect, flash, session

#import MySQLdb

def connection():
    conn = MySQLdb.connect(host= os.getenv('IP'),
                           user = os.getenv('C9_USER'),
                           passwd = "c9",
                           db = "eSports")
    c = conn.cursor()

    return c, conn
    
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register/')
def register():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))
    
    
@app.route('/login/', methods=["GET","POST"])
def login_page():

    error = 'error?'
    try:
        if request.method == "POST":
		
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #flash(attempted_username)
            #flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)  
		
@app.route('/overwatch/')
def overwatch():
    return render_template("overwatch.html")

@app.route('/league/')
def league():
    return render_template("league.html")
    
@app.route('/dota/')
def dota():
    return render_template("dota.html")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
    
@app.errorhandler(405)
def another_error(e):
    return render_template('405.html')

if __name__ == "__main__":

    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))