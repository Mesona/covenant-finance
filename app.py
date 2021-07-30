#!/usr/bin/env python3

from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, flash, g
#from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_session import Session
from database_password import PASSWORD, SECRET_KEY
import psycopg2


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = SECRET_KEY
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcypt = Bcrypt(app)


######################################
def create_connection():
    return psycopg2.connect(user="finance", database="finance", password=PASSWORD)

def create_cursor(connection):
    return connection.cursor()

def close_connections(connection="", cursor=""):
    if connection:
        cursor.close()
    if cursor:
        connection.close()

def initialize_database():
    try:
        connection = create_connection()
        print("CONNECTED!")
    except:
        print("Database connection failed!")

    cursor = create_cursor(connection)

    try:
        login = "create table login (id serial primary key, username varchar(128) unique = True, email varchar(128) unique = True, password varchar(256));"
        covenant = "create table covenant (id serial primary key, name varchar(128), cov json, login_id serial references login(id));"
        cursor.execute(login)
        cursor.execute(covenant)
    except:
        pass

    print("Committing!")
    connection.commit()

    print("Closing!")
    close_database(connection)

def close_database(connection):
    connection.cursor().close()
    connection.close()

def add_user_to_database(cursor, username, email, password):
    cursor.execute("INSERT INTO login (username, email, password) values (%s, %s, %s)", (username, email, password))
    print(f"User {username} added to the database!")

def add_covenant_to_database(covenant):
    #cur.execute("INSERT INTO cov (name, cov, login_id) values (%s, %s, %s)", (covenant.name, covenant, user_id))
    pass

def update_database():
    pass
    #add_user_to_database()
    #add_covenant_to_database()
    #cursor.commit()

def fetch_user_id(cursor, email):
    cursor.execute(f"SELECT id from login where email='{email}';")
    user_id = cursor.fetchone()[0]
    return user_id

######################################

@app.route("/")
def root():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.before_request
def before_request():
    g.username = None
    if "username" in session:
        g.username = session["username"]

@app.route("/home")
def home():
    if g.username:
        return render_template("home.html")
    else:
        return render_template("login.html")
 
@app.route("/authentication", methods=["POST","GET"])
def authenticate():
    import os
    bcrypt = Bcrypt()
 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]   
 
        if session.get("connection") == None:
            session["connection"] = create_connection()
            session["cursor"] = create_cursor(session["connection"])

        session["cursor"].execute("SELECT username,password FROM login WHERE username=%s",[username])

        user = session["cursor"].fetchone()
        username = user[0]
        hashed_pw = user[1]
 
        if len(user) > 0:
            session.pop("username",None)
            if (bcrypt.check_password_hash(hashed_pw, password)) == True:  
                session["username"] = request.form["username"]
                return render_template("home.html", username=username)
            else:
                flash("Invalid Username or Password !!")
                return render_template("login.html")
    else:
        return render_template("login.html")



@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    bcrypt = Bcrypt()

    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        connection = create_connection()
        cursor = create_cursor(connection)
        add_user_to_database(cursor, username, email, bcrypt.generate_password_hash(password).decode("utf-8"))
        connection.commit()

        close_connections(connection, cursor)
        return f"Done!!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
