#!/usr/bin/env python3

import time
import logging
import os
import psycopg2

from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, g
from flask_bcrypt import Bcrypt
from flask_jwt_extended import decode_token, JWTManager
from flask_mail import Mail
from flask_session import Session
from src.covenant import Covenant, save_covenant, load_covenant_from_string
from src.laboratory import Laboratories
from src.covenfolk import Covenfolken, SAVING_CATEGORIES
from src.armory import Armory

app = Flask(__name__)
os.environ['ENV_FILE_LOCATION'] = "./.env"
app.config.from_envvar("ENV_FILE_LOCATION")
mail = Mail(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.secret_key = app.config["APP_SECRET_KEY"]

Session(app)
bcypt = Bcrypt(app)
jwt = JWTManager(app)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger


######################################


def in_gke() -> bool:
    gke_variable = os.environ.get("KUBERNETES_SERVICE_HOST")
    if gke_variable:
        return True

    return False

def create_connection():
    if in_gke():
        return psycopg2.connect(user="finance_owner", database="finance", password=app.config["DATABASE_PASSWORD"], host="192.168.118.110", port="5432")

    return psycopg2.connect(user="finance", database="finance", password=app.config["DATABASE_PASSWORD"])

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

#TODO: Create validation for changing email
#def update_user_email(cursor, user_id, email):
#    cursor.execute("UPDATE login SET email = %s WHERE user_id = %s", (email, user_id))
#    print("Email updated!")

def update_username(cursor, user_id, username):
    cursor.execute("UPDATE login SET username = %s WHERE id = %s;", (username, user_id))
    print("Username updated!")

def update_user_password(user_id, password):
    bcrypt = Bcrypt()
    new_password = bcrypt.generate_password_hash(password).decode("utf-8")

    command = f"UPDATE login SET password = '{new_password}' WHERE id = {int(user_id)};"

    connection = create_connection()
    cursor = create_cursor(connection)

    cursor.execute(command)
    connection.commit()

    close_connections(connection, cursor)
    print("Password updated!")


def update_covenant_in_database(cursor, covenant):
    cursor.execute("UPDATE covenant SET cov = %s WHERE name = %s AND user_id = %s;", (save_covenant(covenant), covenant.name, g.username))


def get_covenant_names(cursor, connection):
    if not session.get("covenant_names"):
        command = f"SELECT name FROM covenant WHERE user_id = '{g.username}'"
        cursor.execute(command, g.username)
        covenant_dump = cursor.fetchall()
        close_database(connection)

        covenant_names = []
        for covenant in covenant_dump:
            name = covenant[0]
            covenant_names.append(name)
        session["covenant_names"] = covenant_names

        return covenant_names
    else:
        return session["covenant_names"]


def append_to_covenant_names(covenant_name):
    session["covenant_names"].append(covenant_name)
    return session["covenant_names"]


def get_user_id_from_email(email):
    connection = create_connection()
    cursor = create_cursor(connection)

    command = f"SELECT id FROM login WHERE email = '{email}';"
    cursor.execute(command, g.username)
    user_id = cursor.fetchone()[0]

    close_connections(connection, cursor)
    return user_id


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
    session["current_covenant"] = None
    session["new_covenant"] = None
    if g.username and not session.get("covenant_names"):
        connection = create_connection()
        cursor = create_cursor(connection)

        user_id_query = f"SELECT id FROM login WHERE username = '{g.username}'"
        cursor.execute(user_id_query)
        user_id = cursor.fetchone()[0]

        user_email_query = f"SELECT email FROM login WHERE username = '{g.username}'"
        cursor.execute(user_email_query)
        user_email = cursor.fetchone()[0]

        covenant_names = get_covenant_names(cursor, connection)

        session["user_id"] = user_id

        session["covenant_names"] = covenant_names  # pylint: disable=assigning-non-slot
        return render_template("home.html", username = g.username, covenants=covenant_names)
    elif g.username and session.get("covenant_names"):
        return render_template("home.html", username = g.username, covenants=session["covenant_names"])
    else:
        return render_template("login.html")


def clean_user_session():
    session["new_covenant"] = False
    session.clear()
    session["current_covenant"] = None
    if g.get("username"):
        g.username = None


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

            return redirect(url_for("home"))
        else:
            flash("Invalid Username or Password !!")
            return render_template("login.html")


@app.route("/advance_covenant", methods=["POST"])
def advance_covenant():
    try:
        disbursement = float(request.form["disbursement"])
    except ValueError:
        disbursement = 0.0

    try:
        singleton_finance_adjustment = float(request.form["singleton_finance_adjustment"])
    except ValueError:
        singleton_finance_adjustment = 0.0

    covenant = session["current_covenant"]
    total_modification = disbursement - singleton_finance_adjustment

    covenant.advance_year(total_modification)

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

    #print("USER ID:", g.username)
    #print("OCVENANT NAME:", covenant_name)
    #print("ARGS:", request.args)
    command = f"SELECT cov FROM covenant WHERE user_id='{g.username}' AND name='{covenant_name}'"
    cursor.execute(command)

    covenant_dump = cursor.fetchall()[0][0]
    #print("DUMP:", covenant_dump)
    #print("DUMP TYPE:", type(covenant_dump))
    covenant = load_covenant_from_string(covenant_dump)
    #print("COVENANT:", covenant)

    connection.commit()
    close_database(connection)

    session['current_covenant'] = covenant
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


@app.route('/forgot_password', methods = ["GET", "POST"])
def forgot_password():
    from src.reset_password import forgotPassword

    if request.method == "GET":
        clean_user_session()
        session.clear()
        #print("IN PAGE")
        #print("REQUEST METHOD:", request.method)
        return render_template('forgot_password.html')
    elif request.method == "POST":
        #print("IN POST")
        #print("REQUEST METHOD:", request.method)
        user_email = request.form['email']
        #print("EMAIL:", user_email)
        user_id = get_user_id_from_email(user_email)
        #print("USER ID:", user_id)

        forgotPassword(user_email, user_id)
        return render_template('login.html')


@app.route('/reset_password/<path:path>', methods = ["GET", "POST"])
def reset_password(path):
    if request.method == "GET":
        clean_user_session()
        session.clear()

        url = request.base_url
        token = url.split("reset_password/")[-1]
        session["token"] = token

        return render_template('reset_password.html', token=token)
    elif request.method == "POST":
        url = request.base_url
        token = session["token"]
        user_id = decode_token(token)['sub']
        #token_expiration = decode_token(token)['exp']

        #if token_expiration < time.time():
        #    raise ValueError("Password reset link has expired! Please request a new one!")

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            raise ValueError("Passwords must match!")

        update_user_password(user_id, password)

        session["token"] = ""

        return redirect("/")


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
    if not session.get("new_covenant") and not session.get("current_covenant"):
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

    if session["current_covenant"].name in session.get("covenant_names") and session.get("new_covenant") is True:
        flash("Covenant names must be unique!")
        return redirect("create_covenant_landing")
    elif not session["new_covenant"]:
        update_covenant_in_database(cursor, session["current_covenant"])
        covenant_names = session["covenant_names"]
    else:
        add_covenant_to_database(cursor, session["current_covenant"])
        covenant_names = append_to_covenant_names(session["current_covenant"].name)

    connection.commit()
    cursor.execute("SELECT * FROM covenant;")
    connection.commit()

    close_database(connection)

    session["new_covenant"] = False
    session["current_covenant"] = None

    return redirect(url_for("home"))


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

        # TODO: Validate lab name is unique and fields are all valid
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
        print("COVENANT SEASON:", session["current_covenant"].season)
        return render_template(
                "modify_covenfolken.html",
                saving_categories=SAVING_CATEGORIES,
                covenant_season=session["current_covenant"].season,
                calculate_servant_minimum=session["current_covenant"].calculate_servant_minimum,
                calculate_teamster_minimum=session["current_covenant"].calculate_teamster_minimum,
                covenant_armory=session["current_covenant"].armory
                )

    if request.method == "POST":
        covenant = session["current_covenant"]

        covenfolken = Covenfolken()

        getlist = request.form.getlist("crafter_name")
        covenfolk_input = request.form.getlist("covenfolk_input")
        non_crafters = ["magi", "companion", "grog", "noble", "dependant", "laborer", "servant", "teamster", "animal"]

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

@app.route("/modify_armory", methods = ["POST", "GET"])
def modify_armory():
    if request.method == "GET":
        current_year = request.args.get("current_year", type = str)
        print("CY:", current_year)
        return render_template("modify_armory.html", saving_categories=SAVING_CATEGORIES, current_year = current_year)

    if request.method == "POST":
        covenant = session["current_covenant"]

        armory = Armory()

        # Handling non magic equipment types
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

        # Handling magic items
        magic = request.form.getlist("magic_name")
        magic_saving_category = request.form.getlist("magic_saving_category")
        magic_saving_value = request.form.getlist("magic_saving_value")
        magic_description = request.form.getlist("magic_description")

        equipment = 0
        print("MAGIC:", magic)
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

        # Handing charged items
        charged = request.form.getlist("charged_name")
        charged_saving_category = request.form.getlist("charged_saving_category")
        charged_saving_value = request.form.getlist("charged_saving_value")
        charged_description = request.form.getlist("charged_description")
        charged_item_activated = request.form.getlist("charged_item_activated")
        charged_item_years_of_charges = request.form.getlist("magic_item_years_worth_of_charges")

        equipment = 0
        while equipment < len(charged):
            armory.add_equipment(
                    charged[equipment],
                    "charged",
                    "magic",
                    charged_saving_category[equipment],
                    int(charged_saving_value[equipment]),
                    charged_description[equipment],
                    True if charged_item_activated[equipment] == "yes" else False,
                    int(charged_item_years_of_charges[equipment]),
            )

            equipment += 1

        covenant.armory = armory

        session["current_covenant"] = covenant

        return render_template("create_covenant_landing.html")

#TODO: Better detection than /var/www
def in_aws():
    """Checks if this is running in an AWS environment."""
    for _, val in os.environ.items():
        if "/var/www" in val:
            return True

    return False

if __name__ == "__main__":
    if in_aws():
        print("IN AWS")
        app.run(host="0.0.0.0", port=5000, debug=True)
    elif in_gke():
        print("IN GKE")
        app.run(host="0.0.0.0", port=5000)
    else:
        print("RUNNING LOCALLY")
        app.run(host="127.0.0.1", port=8000, debug=True)
