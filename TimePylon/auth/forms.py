from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError

from ..models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    remember_me = BooleanField("Eingeloggt bleiben?")
    submit = SubmitField("Einloggen")


class SignupForm(FlaskForm):
    username = StringField("Username",
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp("^[A-Za-z0-9_]{3,}$",
                                      message="Username darf nur aus Buchstaben, Ziffern und Underscores bestehen.")])
    password = PasswordField("Passwort",
                             validators=[
                                 DataRequired(),
                                 EqualTo("password2", message="Passwort-Felder müssen übereinstimmen.")])
    password2 = PasswordField("Passwort bestätigen", validators=[DataRequired()])
    email = StringField("E-Mail",
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError("Es gibt bereits einen Nutzer mit dieser E-Mail-Adresse.")

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError("Username ist bereits vergeben.")
