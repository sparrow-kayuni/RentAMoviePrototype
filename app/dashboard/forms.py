from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length


class CustomerSigninForm(FlaskForm):
    email = EmailField('Customer Email', 
                           validators=[DataRequired('email required!!')])
    submit = SubmitField('SIGN IN')


class CustomerSignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Customer Email', 
                           validators=[DataRequired('email required!!')])
    submit = SubmitField('SIGN UP')