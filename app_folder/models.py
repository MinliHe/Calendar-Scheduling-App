from app_folder import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    '''This class models a user of this application and will hold a users Username and password hash'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    availability = db.relationship("Availability", uselist=False, backref="user")
    meetings = db.relationship("Meetings", uselist=False, backref="user")
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

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

class Meetings(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	length = db.Column(db.String(7), index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Meetings length {}>'.format(self.length)

class listOfMeetings(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingDate = db.Column(db.Integer)
    meetingTime = db.Column(db.Integer)
    descriptionOfMeeting = db.Column(db.String(150))
    participants = db.Column(db.String(64))