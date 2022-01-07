# imports
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, \
    EqualTo


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=15,
               message='Password must be between 6 and 15 characters '
                       'in length')])
    confirm_password = PasswordField(validators=[DataRequired(),
                       EqualTo('password',
                               message='Both passwords must be equal')])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[*?!\'^+%&/()=}\]\[{$#@<>])')
        if not p.match(self.password.data):
            raise ValidationError(
                'Password must contain at least 1 digit, 1 uppercase, '
                'and 1 special character')

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class FavouriteForm(FlaskForm):
    favourite_supplier = StringField(validators=[DataRequired()])
    submit = SubmitField()


class BlacklistForm(FlaskForm):
    blacklist_supplier = StringField(validators=[DataRequired()])
    submit = SubmitField()
