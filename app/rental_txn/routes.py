from flask import render_template, request
from app.rental_txn import rental_txn_bp


@rental_txn_bp.route('/', methods=['GET', 'POST'])
def index():
    # handle rental transaction
    return render_template('rental_txn/index.html')