from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SearchField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Video, Rental

class VideoSearchForm(FlaskForm):
    search = SearchField('Video Title', validators=[DataRequired()])
    submit = SubmitField('LOOK UP')

    def validate_search(self):
        video = Video.query.filter(Video.video_title==self.search).first()
        if not video:
            raise ValidationError('Video doesn\'t exist')
        
        if video.rentals.filter(Rental.date_returned==None).all():
            raise ValidationError('Video isn\'t available')

class CheckoutForm(FlaskForm):
    submit = SubmitField('Checkout')    

class AddVideoForm(FlaskForm):
    submit = SubmitField('Add')

class RemoveVideoForm(FlaskForm):
    submit = SubmitField('Remove') 