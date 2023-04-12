from app import db, login
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    date_returned = db.Column(db.DateTime, default=None)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))

    def __repr__(self):
        return f'<{self.rental_id}, {self.video.video_title}, {self.customer}, {self.date}, {self.due_date}>'


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    videos_rented = db.relationship('Rental', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<{self.customer_id}, {self.first_name} {self.last_name} ,{self.email}>'


class Staff(UserMixin, db.Model):
    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    hashed_password = db.Column(db.String(15), nullable=False)
    rentals_given = db.relationship('Rental', backref='attendant', lazy='dynamic')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return (self.staff_id)

    def __repr__(self):
        return f'<{self.staff_id}, {self.username}>'


@login.user_loader
def load_user(id):
    return Staff.query.get(int(id))

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, nullable=False)
    video_title = db.Column(db.String(20), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    release_year = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)
    rentals = db.relationship('Rental', backref='video', lazy='dynamic')

    def __repr__(self):
        return f'<{self.video_id}, {self.video_title}, {self.unit_price}, {self.genre.genre_name}>'


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre_name = db.Column(db.String(20), nullable=False)
    movies = db.relationship('Video', backref='genre', lazy='dynamic')

    def __repr__(self):
        return f'<{self.genre_id}, {self.genre_name}>'

# class Actor(db.Model):
#     actor_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     actor_name = db.Column(db.String(20))
