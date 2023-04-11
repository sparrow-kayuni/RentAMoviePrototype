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

    totals_spent = {}

    for customer in customers:
        total = 0
        for rental in customer.videos_rented:
            total +=  rental.video.unit_price  + rental.video.unit_price*0.1
        totals_spent[customer.customer_id] = total

    return render_template('customers/index.html', customers=customers, totals_spent=totals_spent)