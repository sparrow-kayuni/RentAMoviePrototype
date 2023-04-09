from flask import render_template, request
from flask_login import login_required, current_user
from app.customers import customers_bp
from app.customers.controllers import CustomersController
from app.customers.errors import NotFoundException

@customers_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    controller = CustomersController()

    try:
        customers = controller.get_customers()
    except NotFoundException():
        customers = []

    return render_template('customers/index.html', customers=customers)