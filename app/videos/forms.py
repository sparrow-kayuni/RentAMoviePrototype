from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange
import datetime
from app.models import Genre

class NewVideoForm(FlaskForm):
    video_title = StringField('Video Title', validators=[DataRequired(), Length(max=60)])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    release_year = IntegerField('Release Year', validators=[DataRequired(), \
                                                           NumberRange(min=1900, max=datetime.date.today().year)])
    genre = SelectField('Genre')
    confirm_checkbox = BooleanField('Tick to confirm new video')
    submit = SubmitField('ADD VIDEO')


class VideoForm(FlaskForm):
    video_title = StringField('Video Title', validators=[DataRequired(), Length(max=60)])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    release_year = IntegerField('Release Year', validators=[DataRequired(), \
                                                           NumberRange(min=1900, max=datetime.date.today().year)])
    genre = SelectField('Genre')
    password = PasswordField('Enter staff password to update changes')
    show_password = BooleanField('Show Password')
    submit = SubmitField('UPDATE VIDEO')

class DeleteForm(FlaskForm):
    password = PasswordField('Enter staff password to delete videos')
    show_password = BooleanField('Show Password')
    submit = SubmitField('DELETE')
