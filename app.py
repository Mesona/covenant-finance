#!/usr/bin/env python3

from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, flash, g
#from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_session import Session
from database_password import PASSWORD, SECRET_KEY
import psycopg2
from covenant import Covenant
from laboratory import Laboratories
from covenfolk import Covenfolken
from armory import Armory


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = SECRET_KEY
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
        connection = create_connection()
        cursor = create_cursor(connection)
        user_id = cursor.execute("SELECT id FROM login WHERE username=%s", [g.username])

        try:
            covenants = cursor.execute("SELECT * FROM covenant WHERE login_id=%s", [user_id])
        except:
            covenants = {}

        return render_template("home.html", username = g.username, covenants = covenants)
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
            connection = create_connection()
            cursor = create_cursor(connection)

        cursor.execute("SELECT username,password FROM login WHERE username=%s",[username])

        user = cursor.fetchone()
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



@app.route('/register')
def register():
    return render_template('register.html')


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
        return redirect(url_for("home"))

@app.route("/create_covenant", methods = ["POST", "GET"])
def create_covenant():
    if request.method == "GET":
        return render_template("create_covenant.html")

    if request.method == "POST":
        name = request.form["covenant_name"]
        season = request.form["covenant_season"]
        income_sources = request.form["covenant_income_sources"]
        tithes = request.form["covenant_tithes"]
        treasury = request.form["covenant_treasury"]
        inflation_enabled = request.form["covenant_inflation_enabled"]
        inflation = request.form["covenant_initial_inflation"]
        current_year = request.form["starting_year"]
        covenant = Covenant(name, season, income_sources, tithes, treasury,
                inflation_enabled, inflation, current_year)
        app.new_covenant = covenant

        return render_template("create_covenant_landing.html")

@app.route("/create_covenant_landing", methods = ["POST", "GET"])
def create_covenant_landing():
    """Shows the current state of the covenant being built. Should have buttons to add equipment, add labs, add covenfolk."""
    if request.method == "GET":
        app.new_covenant.laboratories = Laboratories()
        app.new_covenant.covenfolk = Covenfolken()
        app.new_covenant.armory = Armory()
        return render_template("create_covenant_landing.html")

    if request.method == "POST":
        # Attempt to save cov into DB, assigned to user. Validate cov is configured correctly
        # Reset app.new_covenant
        pass


@app.route("/create_covenant_laboratories", methods = ["POST", "GET"])
def create_covenant_laboratories():
    if request.method == "GET":
        return render_template("create_laboratory.html")

    if request.method == "POST":
        name = request.form["covenant_name"]
        owner = request.form["laboratory_owner"]
        size = request.form["laboratory_size"]
        virtue_points = request.form["virtue_points"]
        flaw_points = request.form["flaw_points"]
        extra_upkeep = request.form["extra_upkeep"]
        usage = request.form["usage"]
        minor_fortifications = request.form["minor_fortifications"]
        major_fortifications = request.form["major_fortifications"]
        # TODO: Validate name is unique and fields are all valid
        app.new_covenant.laboratories.add_lab(name, owner, size, virtue_points, flaw_points,
                extra_upkeep, usage, minor_fortifications, major_fortifications)

        return render_template("create_covenant_landing.html")

@app.route("/create_covenant_covenfolk", methods = ["POST", "GET"])
def create_covenant_covenfolk():
    if request.method == "GET":
        return render_template("create_covenfolk.html")

    if request.method == "POST":
        name = request.form["name"]
        classification = request.form["classification"]
        profession = request.form["profession"]
        saving_category = request.form["saving_category"]
        skill = request.form["skill"]
        rarity = request.form["rarity"]

        app.new_covenant.covenfolk.add_covenfolk(name, classification,
                profession, saving_category, skill, rarity)

        return render_template("create_covenant_landing.html")

@app.route("/create_covenant_armory", methods = ["POST", "GET"])
def create_covenant_armory():
    if request.method == "GET":
        return render_template("create_equipment.html")

    if request.method == "POST":
        name = request.form["name"]
        equipment_type = request.form["equipment_type"]
        quality = request.form["quality"]
        saving_category = request.form["saving_category"]
        saving_value = request.form["saving_value"]
        description = request.form["description"]

        app.new_covenant.armory.add_equipment(name, equipment_type,
                quality, saving_category, saving_value, description)

        return render_template("create_covenant_landing.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
