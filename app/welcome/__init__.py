from app.models import Staff

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class IncorrectUsernameException(Exception):
    pass

class SigninForm(FlaskForm):
    username = StringField('Staff Username', 
                           validators=[DataRequired('username required!!'), 
                                       Length(max=20, message='must be less than 8 letters')])
    password = PasswordField('Staff Password', validators=[DataRequired(), Length(min=6, max=15)])
    show_password = BooleanField('show password')
    submit = SubmitField('SIGN IN')

    def validate_signin(self, form):
        user = Staff.query.filter_by(username=form.username.data).first()
        if not user:
            raise IncorrectUsernameException
            return False
        
        return user.check_password(form.password.data)
