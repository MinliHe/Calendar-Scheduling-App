from flask import render_template
from flask import redirect
from flask import flash, url_for
from app_folder import app, db, login_manager
from .forms import LoginForm, RegistrationForm, DeleteAccountForm, AvailabitityForm, MeetingsForm, ScheduledMeetingForm
from .models import User
import flask_login
import flask
from flask_login import login_user,login_required, logout_user
from wtforms import ValidationError
from flask import request
import datetime
<<<<<<< HEAD
from .models import CustomHTMLCalendar


=======
from flask_wtf import FlaskForm
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeField
>>>>>>> 6f682f54f6397a625e3d6115ee584acd4244c5a0

current_user = flask_login.current_user
cal = CustomHTMLCalendar(0)

@login_manager.user_loader
def load_user(user_id):
    '''
    This method takes the ID of a user and returns the corresponding user object.

    Args:
         user_id (String) : The ID that will be used to find a corresponding user in the data base.

    Returns:
            The user Object that corresponds with the user_id that was passed or none if there is no corresponding user.
    '''
    return User.query.get(int(user_id))

@app.route("/")
@app.route('/index')
# @login_required
def index():
    '''This method creates the webpage that will display when a guest first visits the application.

    Returns:
            The HTML template that will be rendered when a guest first visits the application. This is the home page.
    '''
    return render_template('index.html', title='Home', User=User, current_user=current_user,cal=cal.formatmonth(datetime.date.today().year, datetime.date.today().month))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This method creates the webpage that will display when a guest goes to log into their account.

    Returns:
            the HTML template that will be rendered when a guest wants to log into their account.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('**Invalid username or password**')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    '''
    This method creates the webpage that will display when a guest logs out of the application.

    Returns:
            The HTML template that will be rendered when a guest wants to log out of the application.
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    '''
    This method creates the webpage that will display when a guest wants to create an account.

    Returns:
            The HTML template that will be rendered when a guest wants to create an account.
    '''
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    current_form = RegistrationForm()
    if current_form.validate_on_submit():
        login_user = User(username=current_form.username.data, email=current_form.email.data)
        login_user.set_password(current_form.password.data)
        db.session.add(login_user)
        db.session.commit()
        flash('**Congratulations, you are now a registered user!**')
        return redirect(url_for('login'))
    elif current_form.username.data != None:
        try:
            if 'email' in current_form.errors:
                flash(current_form.errors['email'][0])
            if 'password2' in current_form.errors:
                flash(current_form.errors['password2'][0])
            current_form.validate_username(current_form.username)
            current_form.validate_email(current_form.email)
        except ValidationError as e:
            flash(e)
    return render_template('createAccount.html', title='Create Account', form=current_form)

'''
@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    if request.method == 'POST':
            meetingDate = request.form['meetingDate']
            meetingTime = request.form['meetingTime']
            descriptionOfMeeting = request.form['descriptionOfMeeting']
            participants = request.form['participants']

    db.session.add(meetingDate)
    db.session.commit()

    db.session.add(meetingTime)
    db.session.commit()

    db.session.add(descriptionOfMeeting)
    db.session.commit()

    db.session.add(participants)
    db.session.commit()
    
    return render_template('creatEvent.html', title='Schedule A Meeting', meetingDate = meetingDate, 
                            meetingTime = meetingTime, descriptionOfMeeting = descriptionOfMeeting,
                            participants = participants)
'''
@app.route('/meetingsPage', methods=['GET', 'POST'])
def meetingsPage():
    form = ScheduledMeetingForm()
    return render_template('meetingsPage.html', title='Scheduled Meeting List', form = form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
	delete_acc_form = DeleteAccountForm(request.form)
	availability_form = AvailabitityForm(request.form)
	meetings_form = MeetingsForm(request.form)
	current_user = flask_login.current_user
	if request.method == 'POST':
		if 'Delete Account' == request.form['submit'] :
			db.session.delete(current_user)
			db.session.commit()
			print("Deleting account")
			return redirect(url_for('login'))

		elif 'Set Availability' == request.form['submit']:
			availability = Availability(user_id=current_user.id,from_time=availability_form.from_time.data,to_time=availability_form.to_time.data)
			if current_user.availability:
				availability = Availability.query.get(current_user.availability.id)
				availability.from_time = availability_form.from_time.data
				availability.to_time = availability_form.to_time.data
				db.session.merge(availability)
				db.session.commit()
				print(availability.user)
			else:
				db.session.add(availability)
				db.session.commit()
			print("Setting availability")
			current_user = User.query.get(int(current_user.id))

		elif 'Set Meetings length' == request.form['submit']:
			meetings = Meetings(user_id=current_user.id,length=meetings_form.length.data)
			if current_user.meetings:
				meetings = Meetings.query.get(current_user.meetings.id)
				meetings.length = meetings_form.length.data
				db.session.merge(meetings)
				db.session.commit()
				print(meetings.user)
			else:
				db.session.add(meetings)
				db.session.commit()
			print("Setting meetings length")
			current_user = User.query.get(int(current_user.id))

	return render_template('settings.html', title='Settings', form=delete_acc_form,availability_form=availability_form,user=current_user,meetings_form=meetings_form)
