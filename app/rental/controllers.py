import datetime
from flask_login import current_user
from app import db
from app.models import Customer, Rental, Video, Staff
from app.rental.errors import NotFoundException, NotAvailableException

class RentalController:
    
    def __init__(self):
        pass

    def get_customers(self):
        customers = Customer.query.order_by(Customer.customer_id).all()

        if not customers:
            raise NotFoundException
        
        return customers
    

    def get_customer(self, id):
        customer = Customer.query.filter(Customer.customer_id==id).first()
        if not customer:
            return None

        return customer
    
    def get_available_videos(self):
        videos = []
        # add videos that are available
        for video in Video.query.all():
            if video.rentals.filter(Rental.date_returned==None).all()==[]:
                print(video)
                videos.append(video)
        return videos
    

    def get_video_from_title(self, title):
        video = Video.query.filter(Video.video_title==title).first()

        if not video:
            return None
        
        return video
    
    def check_video_availability(self, video):
        if video.rentals.filter(Rental.date_returned==None).all():
            return False

        return True
    
    def get_video_from_id(self, video_id):
        video = Video.query.filter(Video.video_id==video_id).first()

        if not video:
            return None
        
        return video


    def create_rental(self, vid, customer_id):
        due = datetime.date.today() + datetime.timedelta(weeks=2)
        video = Video.query.get(vid['id'])
        customer = Customer.query.get(customer_id)

        rental = Rental(due_date=due, video=video, attendant=current_user, customer=customer)
        db.session.add(rental)
        db.session.commit()

    def get_rental(self, rental_id):
        rental = Rental.query.filter(Rental.rental_id==rental_id).first()


        return rental
    
    def update_rental(self, rental, customer):
        import datetime
        rental.date_returned = datetime.datetime.utcnow()
        db.session.add(rental)
        db.session.add(customer)
        db.session.commit() 