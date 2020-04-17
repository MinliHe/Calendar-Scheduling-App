from flask import render_template
from flask import redirect
from flask import flash, url_for
from app_folder import app, db, login_manager
from .forms import LoginForm, RegistrationForm
from .models import User
import flask_login
from flask_login import login_user,login_required, logout_user

current_user = flask_login.current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route('/index')
# @login_required
def index():
    return render_template('index.html', title='Home', User=User, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    current_form = RegistrationForm()
    return render_template('createAccount.html', title='Create Account', form=current_form)
