from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SearchField
from wtforms.validators import DataRequired, Length


class VideoSearchForm(FlaskForm):
    search = SearchField('Video Title', validators=[DataRequired()])
    submit = SubmitField('LOOK UP')