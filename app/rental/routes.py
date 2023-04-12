from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

import datetime
from app import db
from app.models import Customer, Rental, Video, Staff
from app.rental.errors import NotFoundException, NotAvailableException
from app.rental import rental_bp
from app.rental.forms import VideoSearchForm

video_cart = {
    'total': 0,
    'items': [],
    'tax': 0.1
}

@rental_bp.route('/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def index(customer_id):
    
    video_search = VideoSearchForm()
    customer_info = {
        'customer': None,
        'videos_rented': []
    }
    video = None
    msg = ''

    if request.method == 'GET':

        customer = Customer.query.filter(Customer.customer_id==customer_id).first()
        if customer:
            customer_info['customer'] = customer
            customer_info['videos_rented'] = customer.videos_rented
        
        import datetime
        default_date = datetime.datetime.utcnow()\
            .replace(year=1000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # when a message parameter is received from any other function(module), 
        # display the message
        if request.args.get('msg'):
            msg = request.args.get('msg')

        # when a video_id parameter is passed(from search function), get the video
        if request.args.get('video_id'):
            video = Video.query.filter(Video.video_id==request.args.get('video_id')).first()

            if not video:
                msg = 'Video doesn\'t exist'
                video=None
        
    return render_template('rental/index.html', video_search=video_search, 
                           video_search_result=video, customer_info=customer_info, msg=msg, 
                           video_cart=video_cart, default_date=default_date)



@rental_bp.route('/<int:customer_id>/search', methods=['GET'])
@login_required
def search(customer_id):
    msg = ''
    video = None
    if request.method == 'GET':
        
        # if there's no search parameter, go back to rental page
        if not request.args.get('search'):
            return redirect(url_for('rental.index', customer_id=customer_id))
        
        video_search = request.args.get('search')
        
        # if search term has an *,  get video using id, if not, get by its title
        if video_search.startswith('*'):
            if not video_search[1:].isnumeric():
                msg = "Enter Numeric Video ID"
                return redirect(url_for('rental.index', customer_id=customer_id, msg=msg))
             
            video = Video.query.filter(Video.video_id==video_search[1:]).first()        
        else:
            video = Video.query.filter(Video.video_title==video_search).first()
        
        # when video isn't found display error message
        if not video:
            msg = 'Video doesn\'t exist'
            return redirect(url_for('rental.index', customer_id=customer_id, msg=msg))

        # after a video result has been found, check if it has been returned
        if video.rentals.filter(Rental.date_returned==None).all():
            msg = 'Video isn\'t currently available'
            return redirect(url_for('rental.index', customer_id=customer_id, msg=msg))

    return redirect(url_for('rental.index', customer_id=customer_id, msg=msg, video_id=video.video_id))


@rental_bp.route('/<int:customer_id>/add/<int:video_id>', methods=['GET'])
@login_required
def add_video(customer_id, video_id):
    global video_cart

    if request.method == 'GET':
        # query videos table for the video to add , create the video object(dict) 
        video = Video.query.filter(Video.video_id==video_id).first() 
        vid = {
            'id': video.video_id,
            'title': video.video_title,
            'unit_price': video.unit_price,
        }

        # when the video to add is already added, display error message, other wise
        # update the video cart items and total
        if vid in video_cart['items']:
            msg='Video already added... Search for another new video'
            return redirect(url_for('rental.index', customer_id=customer_id, msg=msg, video_id=video_id))

        video_cart['items'].append(vid)
        video_cart['total'] += video.unit_price + video.unit_price * video_cart['tax']
    
    return redirect(url_for('rental.index', customer_id=customer_id, video_id=video_id))


@rental_bp.route('/<int:customer_id>/remove/<int:video_id>', methods=['GET'])
@login_required
def remove_video(customer_id, video_id):
    global video_cart

    if request.method == 'GET':
        # same as adding a video, except  we remove the item
        video = Video.query.filter(Video.video_id==video_id).first() 
        vid = {
            'id': video.video_id,
            'title': video.video_title,
            'unit_price': video.unit_price,
        }
        if vid not in video_cart['items']:
            msg='Video isn\'t added inn cart'
            return redirect(url_for('rental.index', customer_id=customer_id, msg=msg))

        video_cart['items'].remove(vid)
        video_cart['total'] -= video_cart['unit_price'] + video_cart['unit_price'] * video_cart['tax']
    
    return redirect(url_for('rental.index', customer_id=customer_id, video_id=video_id))


@rental_bp.route('/<int:customer_id>/checkout')
@login_required
def checkout(customer_id):
    global video_cart

    # loop through all the items in the video cart, then create a rental for each, 
    # which updates the database
    for video in video_cart['items']:
        due_date = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
        due_date.replace(second=0, microsecond=0)
        date = datetime.datetime.utcnow().replace(microsecond=0)
        date_returned = datetime.datetime.utcnow()\
            .replace(year=1000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        video = Video.query.get(video['id'])
        customer = Customer.query.get(customer_id)
        rental = Rental(date=date, due_date=due_date, date_returned=date_returned, \
                        video=video, attendant=current_user, customer=customer)
        db.session.add(rental)
        db.session.commit()
    msg = 'Success'

    # empty the video cart and go to the dashboard
    video_cart['total'] = 0
    video_cart['items'] =  []
    return redirect(url_for('dashboard.index', msg=msg))


@rental_bp.route('/<int:customer_id>/return/<int:rental_id>')
def return_video(customer_id, rental_id):

    if request.method == 'GET':
        # query the customers table to update the specific video the are returning
        customer = Customer.query.filter(Customer.customer_id==customer_id).first()
        
        for rental in customer.videos_rented:
            if rental.rental_id == rental_id:
                import datetime
                rental.date_returned = datetime.datetime.utcnow()\
                    .replace(microsecond=0, second=0)
                db.session.add_all([customer, rental])
                db.session.commit() 
                
    return redirect(url_for('rental.index', customer_id=customer_id))