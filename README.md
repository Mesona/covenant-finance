# covenant-finance
A program for the purpose of yearly advancement and tracking of covenant finances and advancement.

Design Diagram:
![ars finances design diagram](https://drive.google.com/file/d/1FOtXK-c8eIRnU7-4NOxJWv-vT5D7ITbe/view?usp=sharing)

https://lucid.app/lucidchart/2f313fc1-cce1-4b49-97aa-bbb3888e4326/edit?invitationId=inv_9190d9ef-9b74-41b4-82db-e20480a2a77f

To set up your own instance:
  * Prereqs:
    * PSQL
        * `psql`
        * `CREATE DATABASE finance;`
        * `CREATE ROLE finance LOGIN;`
        * `GRANT ALL PRIVILEGES ON DATABASE finance TO finance;`
    * Ensure your database is running off port 5432 (default)
        * If you set a password and/or a secret key, put the values in ./database_password.py
  * Self hosting:
    * Download project
    * `pip install -r requirements.txt`
    * `python -m venv venv`
    * `source venv/bin/activate`
    * `python app.py`
  * Initialize Database Tables:
    * In a python terminal within the virtual env:
      * `from app import initialize_database`
      * `initialize_database()`
  * If using a browser:
    * Open browser to "http://localhost:8000/"
  * If using CLI:
    * `python`
    * `import src.covenant as C`
    * `c = C.Covenant()`
    * Make any modifications
    * `C.save_covenant`

TODO BEFORE BETA:
  * User related:
    * User registration email validation
    * User change password
    * Password recovery
    * Add tooltip to explain 250 income for greater virtue, 100 income for typical
    * Add tooltips to describe different roles under covenfolk (Specialist vs Crafter for example)
    * Add tooltips in general
    * Replace error screens with proper errors
    * Export covenant
    * Cost breakdown by type in covenant page
  * Dev related:
    * Front end tests
    * Fix back end tests, too
    * Add tests for charged items
    * Cap number of covenants a user can have
    * Cap number of income sources a covenant can have
TODO MAYBES BEFORE BETA:
    * Add column in covenfolk to show max savings possible per crafter/specialist

TODO BEFORE RELEASE:
  * Graphics
  * Basic security audit (Cross site forgery, DDOS, etc)
  * Throttle on failed logins
  * Database backup (1 week? 3 weeks?)

BUGS TO FIX:
  * Login with non existant user throws error
  * Fail covenant validation throws error page
  * Fail lab validation (unique name) throws error page
  * Covenant names are currently globally unique, need to be unique per user
  * User's covenants do not populate until new login (create covenant redirect missing data)
  * New Covenent screen's Income Sources +/- button is offset on the first entry for some reason (create multiple and look at the first)
  * Specialsts do not provide savings
