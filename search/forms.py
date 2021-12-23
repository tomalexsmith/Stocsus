from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo


class SearchForm(FlaskForm):
    part_number = StringField(validators=[DataRequired()])
    quantity = StringField(validators=[DataRequired()])
    models = StringField(validators=[DataRequired()])
    submit = SubmitField()
