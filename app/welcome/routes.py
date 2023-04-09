from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse 

from app import rentamovie, db
from app.welcome.forms import SigninForm
from app.welcome.controllers import WelcomeController
from app.welcome.errors import IncorrectUsernameException, IncorrectPasswordException


@rentamovie.route('/')
def index():    
    return render_template('staff/index.html', title='Welcome')


@rentamovie.route('/signin', methods=['GET', 'POST'])
def signin():
    controller = WelcomeController()
    signin_form = SigninForm()
    msg = ''
    
    if signin_form.is_submitted():
        try:
            staff_member = controller.validate_signin(signin_form)
            print(staff_member)
            login_user(staff_member)
            return redirect(url_for('dashboard.index'))           
        except IncorrectUsernameException:
            msg = 'Incorrect User'
        except IncorrectPasswordException:
            msg = f'Incorrect Password {msg}'

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard.index')
       
        
    return render_template('staff/signin.html', title='Staff Sign In', \
                           signin_form=signin_form, error_msg=msg)


@rentamovie.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))