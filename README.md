# calendar-Scheduling-App
Scheduling meetings with others is difficult, and the Calendar Scheduling Application is meant to assist people who have many others who want to meet with them. By providing a space to put their availability and allowing visitors to make an appointment from selecting from the available times, this makes appointments easier to make and more organized.

## Getting Started

The computer should have Python version 3.6 as well as pip installed to setup a localhost web server to serve for the development of the project.

### Prerequisites:

Python 3.6 with pip required extensions:

1. Flask
2. Flask-SQLAlchemy
3. Flask-WTF
4. Flask-Login
5. Flask-Mail
6. Flask-bcrypt
7. WTForms
8. SQLAlchemy
9. Flask-Bootstrap


### Installing

Clone this git repo then install the required extensions. 
Use Terminal to install each extension:

Install Flask:
```
pip install Flask
```
Install flask-wtf, flask-sqlalchemy, flask-login:
```
pip install flask-wtf flask-sqlalchemy flask-login
```
Apply the above command until every extension is installed.

## Running Flask Project

Export the main file of the project by one of two following commands:

For Windows:
```
set FLASK_APP=<filename.py>
```
For Mac:
```
export FLASK_APP=<filename.py>
```

Then, type:
```
flask run
```
