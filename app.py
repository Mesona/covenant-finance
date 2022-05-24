#!/usr/bin/env python3

from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, g
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
import os


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


def in_heroku():
    for key in os.environ.keys():
        if "HEROKU" in key:
            return True

    return False


def create_connection():
    print("AA")
    if in_heroku():
        return psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
        #return psycopg2.connect(user="finance", database="postgresql-polished-48712", password=PASSWORD, sslmode='require')
    else:
        return psycopg2.connect(user="finance", database="finance", password=PASSWORD)
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
    covenant = "CREATE TABLE covenant (id SERIAL PRIMARY KEY, name VARCHAR(128) NOT NULL, cov VARCHAR NOT NULL, user_id VARCHAR(128) NOT NULL);"

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

def update_covenant_in_database(cursor, covenant):
    cursor.execute("UPDATE covenant SET cov = %s WHERE name = %s AND user_id = %s", (save_covenant(covenant), covenant.name, g.username))

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


def get_covenant_names(cursor, connection):
    if not session.get("covenant_names"):
        command = f"SELECT name FROM covenant WHERE user_id=%s"
        cursor.execute(command, g.username)
        covenant_dump = cursor.fetchall()
        close_database(connection)
        print("DUMP:", covenant_dump)

        covenant_names = []
        for covenant in covenant_dump:
            name = covenant[0]
            covenant_names.append(name)
        print("P2:", covenant_names)
        session["covenant_names"] = covenant_names

        return covenant_names
    else:
        return session["covenant_names"]


def append_to_covenant_names(covenant_name):
    session["covenant_names"].append(covenant_name)
    return session["covenant_names"]


######################################

@app.route("/")
def root():
    session["covenant_names"] = None
    print("COVENANT NAMES WIPED:", session["covenant_names"])
    return render_template("login.html")

@app.route("/logout")
def logout():
    clean_user_session()
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
    print("SCN 0:", session.get("covenant_names"))
    session["current_covenant"] = None
    session["new_covenant"] = None
    if g.username and not session.get("covenant_names"):
        print("USERNAME:", g.username)
        connection = create_connection()
        print("a")
        cursor = create_cursor(connection)
        print("b")

        user_id_query = "SELECT id FROM login WHERE username = '%s'"
        print("1")
        cursor.execute(user_id_query, g.username)
        #cursor.execute("SELECT id FROM login WHERE username = {g.username}")
        print("2")
        user_id = cursor.fetchone()[0]
        print("USER_ID", user_id)

        user_email_query = "SELECT email FROM login WHERE username = '%s'"
        cursor.execute(user_email_query, g.username)
        user_email = cursor.fetchone()[0]
        print("USER_EMAIL:", user_email)

        covenant_names = get_covenant_names(cursor, connection)

        session["user_id"] = user_id

        session["covenant_names"] = covenant_names  # pylint: disable=assigning-non-slot
        print("SCN:", session["covenant_names"])
        return render_template("home.html", username = g.username, covenants=covenant_names)
    elif g.username and session.get("covenant_names"):
        print("ALL DATA REQUIRED IS GATHERED")
        return render_template("home.html", username = g.username, covenants=session["covenant_names"])
    else:
        print("OPTION 3")
        return render_template("login.html")


def clean_user_session():
    print("a")
    session["new_covenant"] = False
    print("b")
    session.clear()
    print("c")
    session["current_covenant"] = None
    print("d")
    if g.get("username"):
        g.username = None
    print("e")


@app.route("/authentication", methods=["POST"])
def authenticate():
    import os
    bcrypt = Bcrypt()
    clean_user_session()

    username = request.form["username"]
    password = request.form["password"]

    if session.get("connection") == None:
        connection = create_connection()
        cursor = create_cursor(connection)

    cursor.execute("SELECT username,password FROM login WHERE username=%s",[username])

    user = cursor.fetchone()

    close_database(connection)

    username = user[0]
    hashed_pw = user[1]

    if len(user) > 0:
        session.pop("username",None)
        if (bcrypt.check_password_hash(hashed_pw, password)) == True:  
            session["username"] = request.form["username"]

            #command = f"SELECT name FROM covenant WHERE user_id='{username}'"
            #cursor.execute(command)
            #connection.commit()

            #covenant_dump = cursor.fetchall()
            #close_database(connection)

            #covenant_names = []
            #for covenant in covenant_dump:
            #    name = covenant[0]
            #    covenant_names.append(name)

            return redirect(url_for("home"))
            #return redirect(url_for("home", username=username, covenants=covenant_names))
        else:
            flash("Invalid Username or Password !!")
            return render_template("login.html")


@app.route("/advance_covenant", methods=["POST"])
def advance_covenant():
    try:
        disbursement = float(request.form["disbursement"])
    except ValueError:
        disbursement = 0.0

    covenant = session["current_covenant"]

    covenant.advance_year(disbursement)

    session["current_covenant"] = covenant

    return redirect("create_covenant_landing")


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
        income_sources[income_source] = float(income_value)

    covenant.income_sources = income_sources
    #covenant.tithes = request.form["covenant_tithes"]
    covenant_tithes = {}
    for tithe_source, tithe_value in zip(
            request.form.getlist('tithe_sources_names'),
            request.form.getlist('tithe_sources_values'),
        ):
        covenant_tithes[tithe_source] = float(tithe_value)

    covenant.treasury = float(request.form["covenant_treasury"])
    covenant.inflation_enabled = request.form["covenant_inflation_enabled"]
    covenant.inflation = float(request.form["covenant_initial_inflation"])
    covenant.current_year = int(request.form["current_year"])
    covenant.tithes = covenant_tithes

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
    return redirect("create_covenant_landing")


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
    clean_user_session()
    session.clear()
    return render_template('register.html')


@app.route('/login', methods = ['POST'])
def handle_create_new_user():
    bcrypt = Bcrypt()

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    connection = create_connection()
    cursor = create_cursor(connection)

    cursor.execute("SELECT username, email FROM login")
    connection.commit()
    data = cursor.fetchall()

    if any([ username in i for i in data]) or any([ email in i for i in data]):
        close_connections(connection, cursor)
        flash("Username and email must be unique! Please try another!")
        return render_template("register.html")

    add_user_to_database(cursor, username, email, bcrypt.generate_password_hash(password).decode("utf-8"))
    connection.commit()

    close_connections(connection, cursor)
    return redirect(url_for("home"))

@app.route("/create_covenant", methods = ["GET"])
def create_covenant():
    print("C1:", session.get("new_covenant"))
    print("C1.1:", session.get("current_covenant"))
    if not session.get("new_covenant") and not session.get("current_covenant"):
        session["current_covenant"] = Covenant()
        session["new_covenant"] = True
        print("C1.5:", session.get("new_covenant"))

    if request.method == "GET":
        return render_template("create_covenant.html")

@app.route("/create_covenant_landing", methods = ["POST", "GET"])
def create_covenant_landing():
    """Shows the current state of the covenant being built. Should have buttons to add equipment, add labs, add covenfolk."""
    print("C3:", session.get("new_covenant"))
    if request.method == "GET":
        return render_template("create_covenant_landing.html")

    elif request.method == "POST":
        return render_template("create_covenant_landing.html")

@app.route("/finalize_covenant", methods = ["POST", "GET"])
def finalize_covenant():
    connection = create_connection()
    cursor = create_cursor(connection)

    print("SESSION COVENANT:", session["current_covenant"].name)

    print("C2:", session.get("new_covenant"))
    if session["current_covenant"].name in session.get("covenant_names") and session.get("new_covenant") is True:
        flash("Covenant names must be unique!")
        return redirect("create_covenant_landing")
    elif session["new_covenant"] is False:
        update_covenant_in_database(cursor, session["current_covenant"])
        covenant_names = session["covenant_names"]
    else:
        add_covenant_to_database(cursor, session["current_covenant"])
        covenant_names = append_to_covenant_names(session["current_covenant"].name)

    connection.commit()
    cursor.execute("SELECT * FROM covenant;")
    connection.commit()

    close_database(connection)

    #g.covenant_names = g.covenant_names.append(session["current_covenant"].name)  # pylint: disable=assigning-non-slot
    session["new_covenant"] = False
    session["current_covenant"] = None

    return render_template("home.html", username = g.username, covenants=covenant_names)

    ## TODO: Modularlize 328-337 and DRY from def home()
    #command = f"SELECT name FROM covenant WHERE user_id='{g.username}'"
    #cursor.execute(command)
    #covenant_dump = cursor.fetchall()
    #connection.commit()

    #covenant_names = []
    #for covenant in covenant_dump:
    #    name = covenant[0]
    #    covenant_names.append(name)

    #return render_template("home.html", username=g.username, covenants=covenant_names)

#@app.route("/advance_covenant", methods = ["POST"])
#def advance_covenant():
#    return render_template("create_covenant_landing.html")

@app.route("/modify_laboratories", methods = ["POST", "GET"])
def modify_laboratories():
    if request.method == "GET":
        return render_template("modify_laboratories.html")

    if request.method == "POST":
        covenant = session["current_covenant"]

        labs = Laboratories()

        names = request.form.getlist("laboratory_name")
        owners = request.form.getlist("laboratory_owner")
        sizes = int(request.form.getlist("laboratory_size"))
        virtue_points = int(request.form.getlist("laboratory_virtue_points"))
        flaw_points = int(request.form.getlist("laboratory_flaw_points"))
        extra_upkeeps = int(request.form.getlist("laboratory_extra_upkeep"))
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
        crafter_skills = int(request.form.getlist("crafter_skill"))
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
        specialist_skills = int(request.form.getlist("specialist_skill"))
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
    if in_heroku():
        app.run(host="0.0.0.0", port=os.environ["PORT"], debug=True)
    else:
        app.run(host="127.0.0.1", port=8000, debug=True)
