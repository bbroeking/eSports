import os
from flask import Flask, render_template, url_for, request, redirect, flash, session
from wtforms import Form, TextField, validators, PasswordField, BooleanField
from passlib.hash import sha256_crypt
import gc

try:
    import pymysql
    #pymysql.install_as_MySQLdb()
except ImportError:
    pass

def connection():
    conn = pymysql.connect(host= 'localhost',
                           user = 'root',
                           passwd = 'Qwerty101',
                           db = "eSports")
    c = conn.cursor()

    return c, conn

PandaScoreAPIKey = 'YKbfULoCD_OJaWO9psnXOew9DfVrB2G8CvjOBSA1nlAWziCkNMk'

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            print(str(form.password.data))
            password = sha256_crypt.encrypt(str(form.password.data))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (conn.escape(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, settings, balance) VALUES (%s, %s, %s, %s, %s)",
                          (conn.escape(username), conn.escape(password), conn.escape(email), "", "100"))
                
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('login'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))    
    
@app.route('/login/', methods=["GET","POST"])
def login():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)
		
@app.route('/overwatch/', methods=["GET","POST"])
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
    app.secret_key = 'super secret key'
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))