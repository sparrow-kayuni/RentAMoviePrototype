from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import login, db
from app.models import Customer, Rental, Video, Staff
from app.dashboard.errors import NotFoundException, AlreadyExistsException
from app.dashboard import dashboard_bp
from app.dashboard.forms import CustomerSigninForm, CustomerSignupForm


@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    rentals = []
    msg = ''
    title = 'Dashboard'

    if request.method == 'GET':
        rentals = Rental.query.order_by(Rental.date.desc()).all()
        return_state = {}
        if request.args.get('msg'):
            msg = request.args.get('msg')
        
        if not rentals:
            msg += ' No Rentals to display'

        if msg and msg!='Success':
            return render_template('dashboard/index.html', title=title, rentals=rentals, msg=msg)
        
        import datetime
        default_date = datetime.datetime.utcnow()\
            .replace(year=1000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        for rental in rentals: 
            return_state[rental] = rental.date_returned!=default_date

    return render_template('dashboard/index.html', rentals=rentals, return_state=return_state, msg=msg, title=title)    



@dashboard_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    title = 'Customer Sign In'
    customer_signin = CustomerSigninForm()

    # when email is submitted, validate staff
    if customer_signin.is_submitted():
        customer = Customer.query.filter(Customer.email==customer_signin.email.data).first()
        if not customer:
            msg = 'Customer not Found'
            return render_template('dashboard/signin.html', title=title, customer_signin=customer_signin)
    
        return redirect(url_for('rental.index', customer_id=customer.customer_id))
    
    return render_template('dashboard/signin.html', title=title, customer_signin=customer_signin)


@dashboard_bp.route('signup', methods=['POST', 'GET'])
def signup():
    customer_signup = CustomerSignupForm()
    msg = ''
    title = 'Sign Up'
    customer = Customer.query.filter(Customer.customer_id==0).first()

    # when new customer details are submitted, validate and add new signup then 
    # go to rental page
    if customer_signup.is_submitted():
        if Customer.query.filter(Customer.email==customer_signup.email.data).first():
            msg = 'Customer already exists!!'
            return render_template('dashboard/signup.html', title=title, customer_signup=customer_signup, msg=msg)
        
        customer = Customer(first_name=customer_signup.first_name.data, last_name=customer_signup.last_name.data,
                            email=customer_signup.email.data)
        
        db.session.add(customer)
        db.session.commit()
            
        return redirect(url_for('rental.index', customer_id=customer.customer_id))
    
    return render_template('dashboard/signup.html', title=title, customer_signup=customer_signup)

    
