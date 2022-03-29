#!/usr/bin/env python3

from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, flash, g
#from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_session import Session
from database_password import PASSWORD, SECRET_KEY
import psycopg2
from src.covenant import Covenant, save_covenant, load_covenant_from_string
from src.laboratory import Laboratories
from src.covenfolk import Covenfolken, SAVING_CATEGORIES
from src.armory import Armory
import logging


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = SECRET_KEY
Session(app)
bcypt = Bcrypt(app)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger


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

    login = "CREATE TABLE login (id SERIAL PRIMARY KEY, username VARCHAR(128) UNIQUE NOT NULL, email VARCHAR(128) UNIQUE NOT NULL, password VARCHAR(256) NOT NULL);"
    #covenant = "create table covenant (id serial primary key, name varchar(128), cov json, login_id serial references login(id));"
    covenant = "CREATE TABLE covenant (id SERIAL PRIMARY KEY, name VARCHAR(128) NOT NULL UNIQUE, cov VARCHAR NOT NULL, user_id VARCHAR(128) NOT NULL);"

    try:
        print("CREATING TABLES!")
        cursor.execute(covenant)
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("COVENANT TABLE CREATION ERRORED! DOES IT ALREADY EXIST?")

    try:
        cursor.execute(login)
        connection.commit()
    except psycopg2.errors.DuplicateTable:
        print("LOGIN TABLE CREATION ERRORED! DOES IT ALREADY EXIST?")

    print("Closing!")
    close_database(connection)

def close_database(connection):
    connection.cursor().close()
    connection.close()

def add_user_to_database(cursor, username, email, password):
    cursor.execute("INSERT INTO login (username, email, password) values (%s, %s, %s)", (username, email, password))
    print(f"User {username} added to the database!")

def add_covenant_to_database(cursor, covenant):
    cursor.execute("INSERT INTO covenant (name, cov, user_id) values (%s, %s, %s)", (covenant.name, save_covenant(covenant), g.username))

#def save_covenant_to_database(cursor, covenant):
#    cursor.execute("INSERT INTO cov (name, cov, login_id) values (%s, %s, %s)", (covenant.name, covenant, user_id))
#    pass
#
#def update_database():
#    pass
#    #add_user_to_database()
#    #add_covenant_to_database()
#    #cursor.commit()
#
#def fetch_user_id(cursor, email):
#    cursor.execute(f"SELECT id from login where email='{email}';")
#    user_id = cursor.fetchone()[0]
#    return user_id

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
    g.username = None  # pylint: disable=assigning-non-slot
    if "username" in session:
        g.username = session["username"]  # pylint: disable=assigning-non-slot

@app.route("/home")
def home():
    print("IN HOME")
    if g.username:
        print("g.username EXISTS")
        connection = create_connection()
        cursor = create_cursor(connection)
        user_id = cursor.execute("SELECT id FROM login WHERE username=%s", [g.username])
        user_email = cursor.execute("SELECT email FROM login WHERE username=%s", [g.username])

        print("P1")
        try:
            command = f"SELECT name FROM covenant WHERE user_id='{user_id}'"
            cursor.execute(command)
            covenant_dump = cursor.fetchall()
            connection.commit()
            close_database(connection)

            covenant_names = []
            for covenant in covenant_dump:
                name = covenant[0]
                covenant_names.append(name)
            print("P2")

            session["user_id"] = user_id
            session["cursor"] = cursor
        except:
            covenants = {}

        print("P3")
        return render_template("home.html", username = g.username, covenants=covenant_names)
    else:
        return render_template("login.html")


def clean_session():
    session["new_covenant"] = False
    session["current_covenant"] = None


@app.route("/authentication", methods=["POST","GET"])
def authenticate():
    import os
    bcrypt = Bcrypt()
    clean_session()

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

                command = f"SELECT name FROM covenant WHERE user_id='{username}'"
                cursor.execute(command)
                connection.commit()

                covenant_dump = cursor.fetchall()
                close_database(connection)

                covenant_names = []
                for covenant in covenant_dump:
                    name = covenant[0]
                    covenant_names.append(name)

                return render_template("home.html", username=username, covenants=covenant_names)
            else:
                flash("Invalid Username or Password !!")
                return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/process_new_covenant", methods=["POST"])
def process_new_covenant():
    # Create covenant core
    covenant = session["current_covenant"]

    covenant.name = request.form["covenant_name"]
    covenant.season = request.form["covenant_season"]

    income_sources = {}
    for income_source, income_value in zip(
            request.form.getlist('covenant_income_sources_names'),
            request.form.getlist('covenant_income_sources_values'),
        ):
        income_sources[income_source] = income_value

    covenant.income_sources = income_sources
    covenant.tithes = request.form["covenant_tithes"]
    covenant.treasury = request.form["covenant_treasury"]
    covenant.inflation_enabled = request.form["covenant_inflation_enabled"]
    covenant.inflation = request.form["covenant_initial_inflation"]
    covenant.current_year = request.form["starting_year"]

    # Covenfolk content
    if not hasattr(covenant, "covenfolken"):
        covenant.covenfolk = Covenfolken()

    # Armory content
    if not hasattr(covenant, "armory"):
        covenant.armory = Armory()

    # Laboratory content
    if not hasattr(covenant, "laboratories"):
        covenant.laboratories = Laboratories()

    session['current_covenant'] = covenant
    return render_template("create_covenant_landing.html")


@app.route("/load_existing_covenant", methods=["GET", "POST"])
def load_existing_covenant():
    covenant_name = request.args.get("covenant_name", type = str)

    connection = create_connection()
    cursor = create_cursor(connection)

    print("USER ID:", g.username)
    print("OCVENANT NAME:", covenant_name)
    print("ARGS:", request.args)
    command = f"SELECT cov FROM covenant WHERE user_id='{g.username}' AND name='{covenant_name}'"
    cursor.execute(command)

    covenant_dump = cursor.fetchall()[0][0]
    print("DUMP:", covenant_dump)
    print("DUMP TYPE:", type(covenant_dump))
    covenant = load_covenant_from_string(covenant_dump)
    print("COVENANT:", covenant)

    connection.commit()
    close_database(connection)

    session['current_covenant'] = covenant
    #session['current_covenant'] = covenant_dump
    return render_template("create_covenant_landing.html")


@app.route("/process_covenfolk_modifications", methods=["POST"])
def process_covenfolk_modifications():
    covenant = session["current_covenant"]

    covenfolk = request.form["modify_covenant_covenfolken"]

    return render_template("create_covenant_landing.html")


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
        print("SESSION USERNAME:", username)
        print("SESSION EMAIL:", email)
        connection.commit()

        close_connections(connection, cursor)
        return redirect(url_for("home"))

@app.route("/create_covenant", methods = ["GET"])
def create_covenant():
    if not session.get("new_covenant"):
        session["current_covenant"] = Covenant()
        session["new_covenant"] = True

    if request.method == "GET":
        return render_template("create_covenant.html")

@app.route("/create_covenant_landing", methods = ["POST", "GET"])
def create_covenant_landing():
    """Shows the current state of the covenant being built. Should have buttons to add equipment, add labs, add covenfolk."""
    if request.method == "GET":
        return render_template("create_covenant_landing.html")

    elif request.method == "POST":
        return render_template("create_covenant_landing.html")

@app.route("/finalize_covenant", methods = ["POST", "GET"])
def finalize_covenant():
    connection = create_connection()
    cursor = create_cursor(connection)

    add_covenant_to_database(cursor, session["current_covenant"])
    connection.commit()
    print("Covenant successfully added to database!")
    cursor.execute("SELECT * FROM covenant;")
    connection.commit()
    print("CLOSING CONNECTION")

    # TODO: Modularlize 328-337 and DRY from def home()
    command = f"SELECT name FROM covenant WHERE user_id='{g.username}'"
    cursor.execute(command)
    covenant_dump = cursor.fetchall()
    connection.commit()

    covenant_names = []
    for covenant in covenant_dump:
        name = covenant[0]
        covenant_names.append(name)

    close_database(connection)

    #return render_template("home.html")
    return render_template("home.html", username=g.username, covenants=covenant_names)

@app.route("/advance_covenant", methods = ["POST"])
def advance_covenant():
    return render_template("create_covenant_landing.html")

@app.route("/modify_laboratories", methods = ["POST", "GET"])
def modify_laboratories():
    if request.method == "GET":
        return render_template("modify_laboratories.html")

    if request.method == "POST":
        covenant = session["current_covenant"]

        labs = Laboratories()

        names = request.form.getlist("laboratory_name")
        owners = request.form.getlist("laboratory_owner")
        sizes = request.form.getlist("laboratory_size")
        virtue_points = request.form.getlist("laboratory_virtue_points")
        flaw_points = request.form.getlist("laboratory_flaw_points")
        extra_upkeeps = request.form.getlist("laboratory_extra_upkeep")
        usages = request.form.getlist("usage")
        minor_fortifications = request.form.getlist("laboratory_minor_fortifications")
        major_fortifications = request.form.getlist("laboratory_major_fortifications")

        # TODO: Validate name is unique and fields are all valid
        for i in range(len(names)):
            name = names[i]
            owner = owners[i]
            size = int(sizes[i])
            vp = int(virtue_points[i])
            fp = int(flaw_points[i])
            eu = int(extra_upkeeps[i])
            usage = usages[i]
            min_f = int(minor_fortifications[i])
            maj_f = int(major_fortifications[i])
            labs.add_lab(name, owner, size, vp, fp,
                    eu, usage, min_f, maj_f)

        covenant.laboratories = labs

        session["current_covenant"] = covenant

        return render_template("create_covenant_landing.html")

@app.route("/modify_covenfolken", methods = ["POST", "GET"])
def modify_covenfolken():
    if request.method == "GET":
        return render_template("modify_covenfolken.html", saving_categories=SAVING_CATEGORIES)

    if request.method == "POST":
        covenant = session["current_covenant"]

        form = request.form
        json = request.json
        values = request.values
        data = request.data
        args = request.args
        getlist = request.form.getlist("crafter_name")
        covenfolk_input = request.form.getlist("covenfolk_input")
        non_crafters = ["magi", "companion", "grog", "noble", "dependant", "laborer", "servant", "teamster", "animal"]
        covenfolken = Covenfolken()
        for nc in non_crafters:
            current = f"{nc}_name"
            these_covenfolk = request.form.getlist(current)
            for covenfolk in these_covenfolk:
                if nc == "animal":
                    covenfolken.add_covenfolk(covenfolk, "horse")
                else:
                    covenfolken.add_covenfolk(covenfolk, nc)

        count = 0
        crafter_names = request.form.getlist("crafter_name")
        crafter_professions = request.form.getlist("crafter_profession")
        crafter_saving_categories = request.form.getlist("crafter_saving_category")
        crafter_skills = request.form.getlist("crafter_skill")
        crafter_rarities = request.form.getlist("crafter_rarity")

        while count < len(crafter_names):
            covenfolken.add_covenfolk(
                    crafter_names[count],
                    "crafter",
                    crafter_professions[count],
                    crafter_saving_categories[count],
                    int(crafter_skills[count]),
                    crafter_rarities[count]
            )
            count+=1


        count = 0
        specialist_names = request.form.getlist("specialist_name")
        specialist_professions = request.form.getlist("specialist_profession")
        specialist_saving_categories = request.form.getlist("specialist_saving_category")
        specialist_skills = request.form.getlist("specialist_skill")
        specialist_rarities = request.form.getlist("specialist_rarity")

        while count < len(specialist_names):
            covenfolken.add_covenfolk(
                    specialist_names[count],
                    "specialist",
                    specialist_professions[count],
                    specialist_saving_categories[count],
                    int(specialist_skills[count]),
                    specialist_rarities[count]
            )
            count+=1

        covenant.covenfolken = covenfolken
        session["current_covenant"] = covenant

        return render_template("create_covenant_landing.html")

    #if request.method == "POST":
    #    name = request.form["name"]
    #    classification = request.form["classification"]
    #    profession = request.form["profession"]
    #    saving_category = request.form["saving_category"]
    #    skill = request.form["skill"]
    #    rarity = request.form["rarity"]

    #    app.new_covenant.covenfolk.add_covenfolk(name, classification,
    #            profession, saving_category, skill, rarity)

    #    return render_template("create_covenant_landing.html")

@app.route("/modify_armory", methods = ["POST", "GET"])
def modify_armory():
    if request.method == "GET":
        return render_template("modify_armory.html", saving_categories=SAVING_CATEGORIES)

    if request.method == "POST":
        covenant = session["current_covenant"]

        armory = Armory()

        equipment_types = ["weapon", "partial", "full", "light_siege", "heavy_siege"]
        for equipment_type in equipment_types:
            name = f"{equipment_type}_name"
            quality = f"{equipment_type}_quality"

            equipment_name = request.form.getlist(name)
            equipment_quality = request.form.getlist(quality)

            equipment = 0
            while equipment < len(equipment_name):
                armory.add_equipment(
                        equipment_name[equipment],
                        equipment_type.replace("_", " "),
                        equipment_quality[equipment],
                )

                equipment += 1

        magic = request.form.getlist("magic_name")
        magic_saving_category = request.form.getlist("magic_saving_category")
        magic_saving_value = request.form.getlist("magic_saving_value")
        magic_description = request.form.getlist("magic_description")

        equipment = 0
        while equipment < len(magic):
            armory.add_equipment(
                    magic[equipment],
                    "magic",
                    "magic",
                    magic_saving_category[equipment],
                    magic_saving_value[equipment],
                    magic_description[equipment],
            )

            equipment += 1


        covenant.armory = armory

        session["current_covenant"] = covenant

        return render_template("create_covenant_landing.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
