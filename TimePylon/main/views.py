from flask import render_template
from flask_login import current_user

from . import main
from .. import login_manager
from ..models import User, Entry

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.date).all()
    else:
        entries = []
    return render_template("index.html", entries=entries)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@main.app_errorhandler(403)
def server_error(e):
    return render_template("403.html"), 403