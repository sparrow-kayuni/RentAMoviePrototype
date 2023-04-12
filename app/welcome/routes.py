from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse 

from app import rentamovie, db
from app.models import  Staff, Video, Customer, Genre, Rental
from app.welcome.forms import SigninForm
from app.welcome.errors import IncorrectUsernameException, IncorrectPasswordException


@rentamovie.route('/')
def index():    
    return render_template('staff/index.html', title='Welcome')


@rentamovie.route('/signin', methods=['GET', 'POST'])
def signin():
    signin_form = SigninForm()
    msg = ''
    
    if signin_form.is_submitted():
        staff_member = Staff.query.filter(Staff.username==signin_form.username.data).first()
        
        if not staff_member:
            msg = 'Staff username does\'t exist'
        
        if not staff_member.check_password(signin_form.password.data):
            msg = 'Incorrect Password'

        if msg:
            return render_template('staff/signin.html', title='Staff Sign In', \
                           signin_form=signin_form, msg=msg) 

        login_user(staff_member)      

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard.index')

        return redirect(url_for('dashboard.index'))
    
    return render_template('staff/signin.html', title='Staff Sign In', \
                           signin_form=signin_form) 


@rentamovie.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))