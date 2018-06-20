from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

from . import auth
from .. import db
from .forms import LoginForm, SignupForm
from ..models import User



@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Willkommen, {}! Bitte logge dich ein.".format(user.username))
        return redirect(url_for("auth.login"))
    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Erfolgreich als '{}' eingeloggt.".format(user.username))
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Falscher Benutzer oder Passwort")
    return render_template("login.html", form=form)

