from flask import render_template, request
from flask_login import login_required, current_user

from app.rental import rental_bp
from app.rental.forms import VideoSearchForm
from app.rental.controllers import RentalController
from app.rental.errors import NotFoundException, NotAvailableException

@rental_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    controller = RentalController()
    video_search = VideoSearchForm()
    customer = None
    video = None
    msg = ''

    try:
        if request.args.get('id'):
            customer = controller.get_customer(int(request.args.get('id')))
    except NotFoundException:
        print('Customer wasn\'t found')

    if request.args.get('search'):
        video = controller.get_video_from_title(request.args.get('search'))
        if video:
            if not controller.check_video_availability(video):
                video = None
                msg = 'Video isn\'t currently available'
        else:
            msg = 'Video doesn\'t exist'
        
    return render_template('rental/index.html', video_search=video_search, video=video, 
                           customer=customer, msg=msg)