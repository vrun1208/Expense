from flask import Flask, jsonify, redirect, render_template, request, session, logging, url_for, redirect, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from datetime import datetime
import os
import decimal
from functools import wraps
import expense_table



engine = create_engine("mysql+pymysql://root:@localhost/expense")
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",
                                  {"username": username}).fetchone()
        passworddata = db.execute("SELECT password FROM users WHERE username=:username",
                                  {"username": username}).fetchone()
        userid = db.execute("SELECT user_id FROM users where username=:username",
                                        {"username": username}).fetchone()

        if usernamedata is None:
            flash("No Username!", "danger")
            return render_template("login.html")
        else:
            for password_data in passworddata:
                if sha256_crypt.verify(password,password_data):
                    session['log']=True
                    session['user_id'] = str(userid[0])
                    session['user']=str(username)
                    flash("login successful!","success")
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect Password!","danger")
                    return render_template("login.html")


    return render_template("login.html")



@app.route('/rgt', methods=['GET', 'POST'])
def user_rgt():

    if request.method == 'POST':

        '''adding to database'''

        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm')
        secure_paswword = sha256_crypt.hash(str(password))


        existingUsers = db.execute(
            "SELECT username FROM users WHERE LOWER(username) = :username", {"username": username.lower()}).fetchone()

        if existingUsers:
            flash("Username already taken!","danger")
            return render_template("registration.html")

        if not username:
            return redirect(url_for('user_login'))

        if password == confirm_password:
            db.execute("INSERT INTO users (full_name, username, email_id, password, date) "
                       "VALUES(:full_name, :username, :email_id, :password, :date)",
                       {"full_name": name,"username": username, "email_id": email, "password": secure_paswword, "date": datetime.now()})
            db.commit()

            flash("Registered Successfully!", "success")
            return redirect(url_for('user_login'))
        else:
            flash("Password does not match!","danger")
            return render_template("registration.html")


    return render_template("registration.html")


@app.route('/form', methods=['GET', 'POST'])
def user_expense():
    return render_template("form.html")


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/logout')
def logout():
    session.clear()
    flash("logged Out!","success")
    return render_template("home.html")

@app.route('/add')
def expenses():

    return render_template("add_expense.html")

@app.route('/tab')
def tab():
    results = expense_table.getHistory(session["user_id"])
    return render_template("exp_tab.html", results=results)

@app.route('/exp', methods=['GET', 'POST'])
def add():

    if request.method=="POST":
        form = list(request.form.items())
        if len(form) == 0:
            print("no value :")
            return render_template("add_expense.html")
        else:
            print(form)
            addexpense = expense_table.add_expenses(form, session["user_id"])
            flash("success!", "success")
            return render_template("exp_tab.html", expense=addexpense)
    return None

app.secret_key="qwertyasd123!@#"
app.run(port=5000, host="localhost", debug=True)