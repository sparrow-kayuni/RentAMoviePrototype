from flask import render_template, request
from flask_login import login_required, current_user
from app import db
from app.models import Customer, Rental, Video, Staff
from app.customers import customers_bp
from app.customers.errors import NotFoundException

@customers_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    customers = Customer.query.order_by(Customer.customer_id).all()

    if not customers:
        msg = 'There are currently no customers'
        return render_template('customers/index.html', msg=msg) 

    # store totals in a dictionary
    totals_spent = {}

    # loop through each customer's rentals and add them to to their respective totals 
    for customer in customers:
        total = 0
        for rental in customer.videos_rented:
            total +=  rental.video.unit_price  + rental.video.unit_price*0.1
        totals_spent[customer.customer_id] = total

    return render_template('customers/index.html', customers=customers, totals_spent=totals_spent)