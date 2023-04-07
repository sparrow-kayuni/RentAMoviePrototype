from flask import render_template, request
from app.customers import customers_bp


@customers_bp.route('/', methods=['GET', 'POST'])
def index():
    # view all customers
    return render_template('customers/index.html')