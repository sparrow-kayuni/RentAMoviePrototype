from app import db
from app.models import Customer, Rental, Video, Staff
from app.customers.errors import NotFoundException

class CustomersController:
    
    def __init__(self):
        pass

    def get_customers(self):
        customers = Customer.query.order_by(Customer.customer_id).all()

        if not customers:
            raise NotFoundException
        
        return customers