from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# A FlaskForm containing all the inputs required by user to search for singular part
class SearchForm(FlaskForm):
    part_number = StringField(validators=[DataRequired()])
    quantity = StringField(validators=[DataRequired()])
    models = StringField(validators=[DataRequired()])
    submit = SubmitField()
