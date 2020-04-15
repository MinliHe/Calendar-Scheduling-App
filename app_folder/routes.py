from flask import render_template
from flask import redirect
from flask import flash
from app_folder import app
from .forms import LoginForm, RegistrationForm

# different URL the app will implement
@app.route("/")
# called view function
def hello():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_form = LoginForm()
    if current_form.validate_on_submit():
        flash(f'Login requested for user {current_form.username.data}')
        return redirect('/')
    return render_template('login.html', title='Sign In', form=current_form)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    current_form = RegistrationForm()
    return render_template('createAccount.html', title='Create Account', form=current_form)
