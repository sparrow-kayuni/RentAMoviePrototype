from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import login
from app.dashboard import dashboard_bp
from app.dashboard.controllers import DashboardController
from app.dashboard.forms import CustomerSigninForm, CustomerSignupForm
from app.dashboard.errors import NotFoundException, AlreadyExistsException

controller = DashboardController()

@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    global controller
    rentals = []
    msg = ''

    rentals = controller.get_rentals()
    
    # handle sign request
    return render_template('dashboard/index.html', rentals=rentals, msg=msg)


@dashboard_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    customer_signin = CustomerSigninForm()
    if customer_signin.is_submitted():
        try:
            customer = controller.validate_customer(customer_signin)
            return redirect(url_for('rental.index', id=customer.customer_id))
        except NotFoundException:
            msg = 'Customer not Found'

    return render_template('dashboard/signin.html', customer_signin=customer_signin, msg=msg)


@dashboard_bp.route('signup', methods=['POST', 'GET'])
def signup():
    customer_signup = CustomerSignupForm()
    msg = ''
    if customer_signup.is_submitted():
        try:
            customer = controller.add_new_customer(customer_signup)
            
            return redirect(url_for('rental.index', id=customer.customer_id))
        except AlreadyExistsException:
            msg = '''Customer already Exists'''

    return render_template('dashboard/signup.html', customer_signup=customer_signup, msg=msg)