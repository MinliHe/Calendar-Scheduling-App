# Calendar-Scheduling-App
Getting Started
The computer should have Python version 3.6 as well as pip installed to setup a localhost web server to serve for the development of the project.

Prerequisites:
Python 3.6 with pip required extensions:

Flask
Flask-SQLAlchemy
Flask-WTF
Flask-Login
Flask-Mail
Flask-bcrypt
WTForms
SQLAlchemy
Flask-Bootstrap
Werkzeug
Jinja2
datetime
Installing
Clone this git repo then install the required extensions. Use Terminal to install each extension:

Install Flask:

pip install Flask
Install flask-wtf, flask-sqlalchemy, flask-login:

pip install flask-wtf flask-sqlalchemy flask-login
Apply the above command until every extension is installed.

Running Flask Project
Export the main file of the project by one of two following commands:

For Windows:

set FLASK_APP=<filename.py>
For Mac:

export FLASK_APP=<filename.py>
Then, type:

flask run
