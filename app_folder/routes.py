from flask import render_template
from flask import redirect
from flask import flash
from app_folder import app, db
from .forms import LoginForm, RegistrationForm
from .models import User

@app.route("/")
def hello():
    return render_template('index.html', title='Home', User=User)

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_form = LoginForm()
    try:
        if (current_form.validate_on_submit() and
              current_form.validate_account(current_form.username.data, current_form.password.data)):
            flash(f'{current_form.username.data} just logged in.')
            return redirect('/')
    except:
        flash(f'Login credentials are incorrect. Please try again.')
    return render_template('login.html', title='Sign In', form=current_form)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    current_form = RegistrationForm()
    return render_template('createAccount.html', title='Create Account', form=current_form)
