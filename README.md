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
## Features

### Register
a user must have an account to access the web app. New users can create their own personal accounts by entering their name, a valid email address, and a password. Once registered, the user's credentials are saved via MySQL Database and will allow the user to login at any time. 

### Login
Existing users who have made accounts can log into the web app to access its features. Once a user is logged in, they are redirected to the homepage where they will be able to create, delete, change a calendar and logout.

### Logout 
Users who are logged into the web app can log out too. Logging out will save the user's information until the next login via database. 

### Creating An Event
Creating an event is the main feature of this web app. Users enter a day/time, and leave a brief event description.A warning message will show to the users if there two events are overlapped before users hit the submit button. After hitting the submit button, the information of this event will be stored to the database.

### View An Event
Event after being created will be display in the homepage. After the users hit submit to create the new event, they will be immediately carried to he homepage to see what they've just created as well as the list of old events. Events displayed in the homepage will include the information the users input such as title, date, time, description.

### Edit An Event
Users have the ability to fix any information about the event. By hitting the edit button below the event on the homepage, the edit form will be displayed to let the users decide what they want to keep and change. After hitting the submit button, it will go back to the homepage and display the event after editing.  

### Delete Event
Users have the ability to delete events they no longer want to keep track of. By hitting the delete button below the event on the homepage, the event will be removed.

### Share
Users have the ability to send a message to ask other users who want to join this event through email.

### Check Event
In this feature, users have the ability to classify which event is coming and which event is Expired. The Expired event will be displayed in a column beside the column storing Expired events. Users can also check how many people will join this event.

### Share
Users have the ability to send a message to ask other users who want to join this event through email.


## Testing location: 

## Sphinx Documentation location: 


## Author
* **Shana Nguyen**
* **Hao Tu**
* **Minli He**
* **Jonathan Aguayo**
