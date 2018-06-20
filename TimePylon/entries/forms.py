from flask_wtf import FlaskForm
from wtforms.fields import StringField, TimeField, IntegerField, DateField
from wtforms.validators import InputRequired

class EntryForm(FlaskForm):
    date = DateField(label="Datum", validators=[InputRequired()], format='%d.%m.%Y')
    start = TimeField(label="Beginn", validators=[InputRequired()])
    end = TimeField(label="Ende", validators=[InputRequired()])
    pause = IntegerField(label="Pause", validators=[InputRequired()])
    comment = StringField(label="Kommentar")
