from flask import render_template
from flask import redirect
from flask import flash, url_for
from app_folder import app, db, login_manager
from .forms import LoginForm, RegistrationForm, DeleteAccountForm, AvailabitityForm, MeetingsForm, EmailConfirmationForm, AppointmentForm
from .models import User, Availability,Meetings, listOfMeetings, CustomHTMLCalendar
import flask_login
import flask
from flask_login import login_user,login_required, logout_user
from wtforms import ValidationError
from flask import request
import datetime
from flask_mail import Mail, Message



current_user = flask_login.current_user
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '2020131springteam6@gmail.com'
app.config['MAIL_PASSWORD'] = 'abc!123ab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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
def index():
    '''This method creates the webpage that will display when a guest first visits the application.

    Returns:
            The HTML template that will be rendered when a guest first visits the application. This is the home page.
    '''
    return render_template('index.html', title='Home', User=User, current_user=current_user)

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

import time

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
'''
@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    if request.method == 'POST':
        try:
            meetingDate = request.form['meetingDate']
            meetingTime = request.form['meetingTime']
            descriptionOfMeeting = request.form['descriptionOfMeeting']
            participants = request.form['participants']

        db.session.add(meetingDate)
        db.session.commit()
    if meetingDate >= datetime.utcnow :
        db.session.add(meetingDate)
        db.session.commit()
    else:
        flash('Pleasse choose another date and time.')

    db.session.add(meetingTime)
    db.session.commit()
    if meetingTime >= datetime.utcnow :
        db.session.add(meetingTime)
        db.session.commit()
    else:
        flash('Pleasse choose another date and time.')

    db.session.add(descriptionOfMeeting)
    db.session.commit()

    db.session.add(participants)
    db.session.commit()

    return render_template('creatEvent.html', title='Schedule A Meeting', meetingDate = meetingDate,
                            meetingTime = meetingTime, descriptionOfMeeting = descriptionOfMeeting,
                            participants = participants)
'''
@login_required
@app.route('/meetingsPage', methods=['GET', 'POST'])
def meetingsPage():
    appointments_list = None
    if not current_user.is_anonymous and current_user.appointments != None :
        appointments_list = current_user.appointments.query.filter_by(user_id = current_user.id)
    return render_template('meetingsPage.html', title='Scheduled Meeting List', current_user=current_user, appointments_list=appointments_list)
    # return render_template('createEvent.html', title='Schedule A Meeting', form = form)

@login_required
@app.route('/settings', methods=['GET', 'POST'])
def settings():
	delete_acc_form = DeleteAccountForm(request.form)
	availability_form = AvailabitityForm(request.form)
	email_confirmation_form = EmailConfirmationForm(request.form)
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
			if not isTimeFormat(availability_form.from_time.data) or not  isTimeFormat(availability_form.to_time.data) or availability_form.from_time.data > availability_form.to_time.data:
				flash('**Invalid availability!**')
			else:
				if not time_in_range("09:00","22:00",availability_form.from_time.data) or not time_in_range("09:00","22:00",availability_form.to_time.data):
					flash('**Invalid range choose between 09:00 am  and 10:00 pm!**')
				else:
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
			if  str(meetings_form.length.data) != "00:15" and str(meetings_form.length.data) != "00:30" and str(meetings_form.length.data) != "01:00" :
				flash("use 00:15, 00:30 minutes or 01:00 hour  slots"+str(meetings_form.length.data)+ str(str(meetings_form.length.data) == "00:15"))
			else:
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
		elif 'Set Email Confirmation' == request.form['submit']:
			current_user.email_confirmation = email_confirmation_form.confirmation.data
			db.session.merge(current_user)
			db.session.commit()
			current_user = User.query.get(int(current_user.id))

			msg = Message('Hello', sender = '2020131springteam6@gmail.com', recipients = ['thllmxx@gmail.com'])
			msg.body = "Hello Flask message sent from Flask-Mail"
			mail.send(msg)


	return render_template('settings.html', title='Settings', form=delete_acc_form,availability_form=availability_form,user=current_user,meetings_form=meetings_form,email_form=email_confirmation_form)


@app.route('/<userpage>', methods=['GET', 'POST'])
def show_user_cal(userpage):
    '''
    This method takes a username and loads the users event calendar.

    Args:
         userpage (String) : The username that will be checked for validity in the data base and used as the url.

    Returns:
            The users event calendar if the username that was passed corresponds to a valid user.
            Otherwise, this method will return an html page saying the page does not exist.
    '''
    userscal = User.query.filter_by(username=userpage).first()
    cal = CustomHTMLCalendar()
    cal.set_username(userpage)
    if userscal is None:
        return render_template('404.html', badurl=userpage)
    else:
        return render_template('calendar.html', user=userpage,cal=cal.formatmonth(datetime.date.today().year, datetime.date.today().month))

@app.route('/<userpage>/<day>', methods=['GET', 'POST'])
def createAppointment(userpage, day):
    current_form = AppointmentForm()
    userscal = User.query.filter_by(username=userpage).first()
    if userscal is None:
        return render_template('404.html', badurl=userpage)
    availability = userscal.availability
    meetings = userscal.meetings
    if availability != None:
        current_form.times.choices = availability.set_available_times(availability.from_time, meetings.length, availability.to_time)

    if current_form.validate_on_submit():
        try:
            appointments = listOfMeetings(
                user_id=userscal.id,
                meetingDate="{}/{}".format(datetime.date.today().month,day),
                meetingTime=current_form.times.data,
                participants=current_form.person.data,
                descriptionOfMeeting=current_form.details.data)
            db.session.merge(appointments)
            db.session.commit()
            flash("** Successfully Created Appointment! **")
        except ValidationError as e:
            flash(e)

    return render_template('createAppointment.html', user=userpage, month=datetime.date.today().month, day=day, form=current_form, availability=availability, meetings=meetings)
