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