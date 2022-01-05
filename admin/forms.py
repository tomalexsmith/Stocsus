from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class BanForm(FlaskForm):
    email_to_ban = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()


class UnbanForm(FlaskForm):
    email_to_unban = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()
