from app_folder import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from calendar import HTMLCalendar
from flask import url_for

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    '''This class models a user of this application and will hold a users Username and password hash'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    sendEmailConfirm = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    availability = db.relationship("Availability", uselist=False, backref="user")
    meetings = db.relationship("Meetings", uselist=False, backref="user")
    appointments = db.relationship("listOfMeetings", uselist=False, backref="user")
    usercal = db.relationship("CustomHTMLCalendar", uselist=False, backref="user")
    posts = db.relationship('Post', backref="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def print_username(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        ''' This functions generates a hash based on a users account password.

            Args:
                 password (String) : The password that a user chooses to associate with their account.
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        ''' This function checks if a input password corresponds with the hash associated with the account.

            Args:
                 password (String) : The password that will be checked.

            Returns:
                    True if the password corresponds with the hash associated with the users account.
        '''
        return check_password_hash(self.password_hash, password)


class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Posts {}>'.format(self.body)

class Availability(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_time = db.Column(db.String(7), index=True, default=datetime.utcnow)
    to_time = db.Column(db.String(7), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Availability from  {} to {}>'.format(self.from_time,self.to_time)

    # calculates the endtime of an appointment based off of the start time and meeting duration
    def calculateEndTime(self, apptStartTime, meetingLength):
        splitTime = apptStartTime.split(':')
        splitMeetingminutes = meetingLength.split(':')
        if int(splitMeetingminutes[0]) == 1:
            endHour = int(splitTime[0]) + 1
            endTime = str(endHour) + ':' + str(splitTime[1])
        else:
            endMinutes = int(splitTime[1]) + int(splitMeetingminutes[1])
            if endMinutes >= 60:
                endMinutes = endMinutes - 60
                endHour = int(splitTime[0]) + 1
                if endMinutes < 10 and endMinutes != 0:
                    endTime = str(endHour) + ':0' + str(endMinutes)
                elif endMinutes == 0:
                    endTime = str(endHour) + ':00'
                else:
                    endTime = str(endHour) + ':' + str(endMinutes)
            else:
                endHour = splitTime[0]
                endTime = str(endHour) + ':' + str(endMinutes)
        return endTime

    # checks to see if the endtime is not past the user's available times
    def in_range(self, availableEndTime, apptEndTime):
        splitAvailEnd = availableEndTime.split(':')
        splitApptEnd = apptEndTime.split(':')
        # comparing end times of availability and appointment
        endAvailInt = int(splitAvailEnd[0]) * 100 + int(splitAvailEnd[1])
        endApptInt = int(splitApptEnd[0]) * 100 + int(splitApptEnd[1])
        if endAvailInt < endApptInt:
            return False
        else:
            return True


    # add to an array to hold all the possible meeting intervals
    def set_available_times(
        self,
        start_time,
        incrementAmount,
        end_time,
        ):
        availAppts = []
        apptEndTime = self.calculateEndTime(start_time, incrementAmount)
        apptStartTime = start_time
        while self.in_range(end_time, apptEndTime):
            appointmentTime = apptStartTime + ' - ' + apptEndTime
            availAppts.append((appointmentTime, appointmentTime))
            apptStartTime = apptEndTime
            apptEndTime = self.calculateEndTime(apptStartTime, incrementAmount)
        return availAppts

    def remove_busy_times(self, apptArray, listOfMadeMeetingsArray):
        #this gets an array of the appointments that that user has on that day
        something = []
        for times in listOfMadeMeetingsArray:
            if ((times.meetingTime, times.meetingTime)) in apptArray:
                apptArray.remove((times.meetingTime, times.meetingTime))
        return apptArray


class Meetings(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	length = db.Column(db.String(7), index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Meetings length {}>'.format(self.length)

class listOfMeetings(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingDate = db.Column(db.String)
    meetingTime = db.Column(db.String)
    descriptionOfMeeting = db.Column(db.String(150))
    participants = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Appointment with{}, on {} from {}>'.format(self.participants, self.meetingDate, self.meetingTime)

class CustomHTMLCalendar(UserMixin, HTMLCalendar, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # It's not being linked to the other table

    username = ""
    def set_username(self, user):
        self.username = user

    def formatday(self, day, weekday):
        """This method returns a line of html that is used to create the calendar. Each date of the calendar is a link that will open a new page and redirect you to google.com
           This link can be changed to redirect to another website later on.

           Args:
                day (String): The date, such as 1, 2, 3 etc.
                weekday (String): The day of the week such as mon, tue, wed, etc.
           Returns:
                   A string corresponding to the html code that should be written for each day in the month. If the day is 0, this method will return html code to be blank.
                   If the day is within the date range of the month, the method will return the html to represent the day of the month with each day being a link.
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            return '<td class="%s"><a href="%s" target="_blank">%d</a></td>' % (self.cssclasses[weekday], "{}/{}".format(self.username, day), day)
