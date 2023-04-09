from app import db
from app.models import  Staff, Video, Customer, Genre, Rental
from app.welcome.errors import IncorrectUsernameException, IncorrectPasswordException, NotFoundException

def init_data():
    db.drop_all()
    db.create_all()

    s1 = Staff(username='lydia.mtonga')
    s1.set_password('HerHighNess')
    db.session.add(s1)

    s2 = Staff(username='michael.chibangwe')
    s2.set_password('BoysALawyerBwooyy')
    db.session.add(s2)

    genres = [Genre(genre_name=genre) for genre in \
            ['Horror', 'Action','Sci-Fi', 'Comedy', 'Romance', 'Adventure', 'Drama', 'Kids', 'Nature', 'Documentary', 'Edutainment']]

    db.session.add_all(genres)

    videos = [Video(video_title=title, unit_price=price, release_year=year, genre=gen) \
            for (title, price, year, gen, avail) in [
                ('Fantastic Four', 12.5, 2008, genres[2], True),
                ('Mega-Beasts', 10, 2010, genres[4], True),
                ('David And Goliath', 13, 2014, genres[1], False),
                ('Max', 15, 2021, genres[6], True),
                ('Light', 15, 2022, genres[5], False),
            ]]

    db.session.add_all(videos)

    customers = [Customer(first_name=fname, last_name=lname, email=em) \
                 for (fname, lname, em) in [
                    ('Chileshe', 'Bwalya', 'cbwalya@gmail,com'),
                    ('Nina', 'Daryll', 'darryll@nina.com')
                ]]

    db.session.add_all(customers)

    import datetime
    due = datetime.date.today() + datetime.timedelta(weeks=2)
    
    rentals = [Rental(due_date=due, video=videos[i], attendant=s1, customer=customers[0]) \
               for i in range(3)]

    db.session.add_all(rentals)

    customers[0].videos_rented = rentals

    db.session.commit()

class WelcomeController:
    def __init__(self):
        pass

    # def get_staff(self):
    #     staff = Staff.query.all()

    #     if not staff:
    #         raise NotFoundException

    def validate_signin(self, form):
        staff = Staff.query.filter(Staff.username==form.username.data).first()
        if not staff:
            raise IncorrectUsernameException
        
        if not staff.check_password(form.password.data):
            raise IncorrectPasswordException
        
        return staff