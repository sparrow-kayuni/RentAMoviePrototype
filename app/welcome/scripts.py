from app import db
from app.models import  Staff, Video, Customer, Genre, Rental
from app.welcome.errors import IncorrectUsernameException, IncorrectPasswordException, NotFoundException


def init_data():
    db.drop_all()
    db.create_all()

    s1 = Staff(username='lydia.mtonga')
    s1.set_password('HerHighNess')

    s2 = Staff(username='michael.chibangwe')
    s2.set_password('BoysALawyerBwooyy')
    db.session.add_all([s1, s2])

    genres = [Genre(genre_name=genre) for genre in \
            ['Horror', 'Action','Sci-Fi', 'Comedy', 'Romance', 'Adventure', 'Drama', 'Kids', 'Nature', 'Documentary', 'Edutainment']]

    db.session.add_all(genres)

    videos = [Video(video_title=title, unit_price=price, release_year=year, genre=gen) \
            for (title, price, year, gen) in [
                ('Fantastic Four', 12.5, 2008, genres[2]),
                ('Mega-Beasts', 10, 2010, genres[4]),
                ('David And Goliath', 13, 2014, genres[1]),
                ('Max', 15, 2021, genres[6]),
                ('Light', 15, 2022, genres[5]),
                ('12 Mighty Orphans', 13.5, 2022, genres[5]),
                ('1917', 10, 2019, genres[1]),
                ('A Day To Die', 13, 2022, genres[1]),
                ('Afterlife of the Party', 15, 2021, genres[6]),
                ('Agent Game', 12, 2022, genres[5]),
                ('Fantastic Four', 12.5, 2008, genres[2]),
                ('Black Adam', 15, 2022, genres[1]),
                ('Boss Level', 13, 2020, genres[3]),
                ('Coda', 15, 2021, genres[6]),
                ('Constantine', 10, 2005, genres[1]),
                ('Dangerous Lies', 11, 2020, genres[6]),
                ('Holiday Monday', 12, 2021, genres[5]),
                ('Enola Holmes', 12.5, 2022, genres[2]),
                ('Lost Girls', 14, 2020, genres[3]),
                ('Mile 22', 13, 2018, genres[0]),
                ('Sicario', 13, 2015, genres[1]),
                ('Sicario Day Of The Soldado', 15, 2015, genres[1]),
                ('Rogue Hostage', 13, 2021, genres[0]),
                ('Spider-Man No Way Home', 15, 2021, genres[1]),
                ('Stillwater', 12, 2021, genres[6]),
                ('The Northman', 15, 2022, genres[3])
            ]]

    db.session.add_all(videos)
    
#     default_customer = Customer(customer_id=0, first_name='', last_name='', email='')
#     default_staff = Staff(staff_id=0, username='', hashed_password='no password')
#     default_genre = Genre(genre_id=0, genre_name='')
#     default_video = Video(video_id=0, video_title='', unit_price=0, release_year=0, genre=default_genre)
#     default_rental = Rental(rental_id=0, date=None, due_date=None, customer=default_customer, \
#                         video=default_video, attendant=default_staff)
    
#     db.session.add_all([default_customer, default_genre, default_video,  default_rental, default_staff])

    db.session.commit()