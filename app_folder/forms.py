from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired, Email, DataRequired, EqualTo
from .models import User

class LoginForm(FlaskForm):
    '''This class defines the form that will be seen when a user tries to log into the Calendar-Scheduling-App.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def check_password(self, username, password):
        '''This method takes the inputs from the LoginForm text fields and checks if password is associated with the username.

           Args:
                username (String) : The username that will be used to retrieve an assocated password hash.

                password (String) : The password that will be turned into a hash and be compared with the usernames associated password hash.

           Returns:
                   True if the password that was passed matches the password assosicated with the username that was passed.

                   False if the password that was passed does not match the password associated wiht the username that was passed.


        '''
        user = User.query.filter_by(username=username).first()
        if user.password_hash == password:
            return True
        else:
            return False

class RegistrationForm(FlaskForm):
    '''This class defines the form that will be seen when a user tries to register an account in the Calendar-Scheduling-App
    '''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message="Passwords do not match.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        '''
        This method checks if the username is still available and will raise an error if it is not.

        Args:
            username (String) : The username that will be checked for availability in the data base.
        '''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''
        This method checks if the email addresss that is passed is still available and will raise an error if it is not.

        Args:
            email (String) : The email that will be checked for availability in the data base.
        '''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DeleteAccountForm(FlaskForm):
	submit = SubmitField('Delete Account')

class AvailabitityForm(FlaskForm):
	from_time = StringField('From time', validators=[DataRequired()])
	to_time = StringField('From time', validators=[DataRequired()])
	submit = SubmitField('Set Availability')

class MeetingsForm(FlaskForm):
	length = StringField('Length of meetings', validators=[DataRequired()])
	submit = SubmitField('Set Meetings length')
