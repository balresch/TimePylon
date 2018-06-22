from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, DateField
from wtforms.validators import InputRequired

class DatepickForm(FlaskForm):
    datepick = DateField(label="Monat.Jahr", validators=[InputRequired()], format='%m.%Y')
    submit = SubmitField("Bestätigen")
