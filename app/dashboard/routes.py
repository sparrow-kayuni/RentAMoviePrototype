from flask import render_template, request
from app.dashboard import dashboard_bp


@dashboard_bp.route('/', methods=['GET', 'POST'])
def index():
    # handle sign in request

    # handle sign request
    return render_template('dashboard/index.html')