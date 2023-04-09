from app import db
from app.models import Customer, Rental, Video, Staff
from app.dashboard.errors import NotFoundException, AlreadyExistsException

class DashboardController:
    
    def __init__(self):
        pass

    def get_rentals_query(self):
        rentals = Rental.query.order_by(Rental.date.desc()).all()       

        if not rentals:
            raise NotFoundException
            pass

        return rentals


    def get_staff_member_query(staff_id):
        member = Staff.query.filter(Staff.staff_id==staff_id).first()

        if not member:
            raise NotFoundException
        return member


    def get_rentals(self):
        rentals = []
        try:
            rental_txns = self.get_rentals_query()
        except NotFoundException:
            rentals = []
        finally:
            return rental_txns

    def validate_customer(self, form):
        customer = Customer.query.filter(Customer.email==form.email.data).first()
        if not customer:
            raise NotFoundException
        
        return customer
    
    def get_customer(self, id):
        customer = Customer.query.filter(Customer.customer_id==id).first()
        if not customer:
            raise NotFoundException

        return customer
        

    def add_new_customer(self, form):
        if Customer.query.filter(Customer.email==form.email.data).first():
            print('Already exists!!')
            raise AlreadyExistsException
        
        customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data,
                            email=form.email.data)
        
        db.session.add(customer)
        db.session.commit()

        return customer

