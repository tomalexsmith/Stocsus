# imports
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length, \
    EqualTo


# checks for the excluded characters
def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email])
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


class login_form(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField()

class search_form(FlaskForm):
    part_number = StringField(validators=[Required()])
    quantity = StringField(validators=[Required()])
    models = StringField(validators=[Required()])
    submit = SubmitField()
