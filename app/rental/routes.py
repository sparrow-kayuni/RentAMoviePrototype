from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.rental import rental_bp
from app.rental.forms import VideoSearchForm
from app.rental.controllers import RentalController
from app.rental.errors import NotFoundException, NotAvailableException

customer = None
video_cart = []
total = 0
controller = RentalController()

@rental_bp.route('/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def index(customer_id):
    
    video_search = VideoSearchForm()
    global customer
    global total
    video = None
    msg = ''

    if request.method == 'GET':

        customer = controller.get_customer(customer_id)

        if request.args.get('msg'):
            msg = request.args.get('msg')

        if request.args.get('video_id'):
            video = controller.get_video_from_id(request.args.get('video_id'))
            print(video)
            if video:
                pass

        
    return render_template('rental/index.html', video_search=video_search, checkout=checkout, 
                           video_search_result=video, customer=customer, msg=msg, 
                           video_cart=video_cart, total=total)


@rental_bp.route('/<int:customer_id>/search', methods=['GET'])
@login_required
def search(customer_id):
    msg = ''
    video = None
    if request.method == 'GET':
        customer = controller.get_customer(customer_id)

        video_search = request.args.get('search')
        if video_search.startswith('*'):
            print(video_search[1:])
            if video_search[1:].isnumeric():
                video = controller.get_video_from_id(int(video_search[1:]))
            else:
                msg = "Enter Numeric Video ID"
        else:
            video = controller.get_video_from_title(video_search)
        
        if video:
            if controller.check_video_availability(video):
                return redirect(url_for('rental.index', customer_id=customer_id, msg=msg, video_id=video.video_id))
            
            video = None
            msg = 'Video isn\'t currently available'
        else:
            msg = 'Video doesn\'t exist'
    print(msg)
    return redirect(url_for('rental.index', customer_id=customer_id, msg=msg))


@rental_bp.route('/<int:customer_id>/add/<int:video_id>', methods=['GET'])
@login_required
def add_video(customer_id, video_id):
    global video_cart
    global total

    if request.method == 'GET':
        video = controller.get_video_from_id(video_id)
        vid = {
            'id': video.video_id,
            'title': video.video_title,
            'unit_price': video.unit_price
        }
        if vid not in video_cart:
            video_cart.append(vid)
            total += video.unit_price
    
    return redirect(url_for('rental.index', customer_id=customer_id, video_id=video_id))


@rental_bp.route('/<int:customer_id>/remove/<int:video_id>', methods=['GET'])
@login_required
def remove_video(customer_id, video_id):
    global video_cart
    global total
    
    if request.method == 'GET':
        video = controller.get_video_from_id(video_id)
        vid = {
            'id': video.video_id,
            'title': video.video_title,
            'unit_price': video.unit_price
        }
        if vid in video_cart:
            video_cart.remove(vid)
            total -= video.unit_price
    
    return redirect(url_for('rental.index', customer_id=customer_id))


@rental_bp.route('/<int:customer_id>/checkout')
@login_required
def checkout(customer_id):
    global video_cart
    for video in video_cart:
        controller.create_rental(video, customer_id)
    video_cart = []
    total = 0
    return redirect(url_for('dashboard.index'))