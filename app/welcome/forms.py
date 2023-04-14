from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class SigninForm(FlaskForm):
    username = StringField('Staff Username', 
                           validators=[DataRequired('username required!!'), 
                                       Length(max=20, message='must be less than 8 letters')])
    password = PasswordField('Staff Password', validators=[DataRequired(), Length(min=4, max=30)])
    show_password = BooleanField('show password')
    submit = SubmitField('SIGN IN')
