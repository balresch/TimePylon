from datetime import timedelta

from flask import render_template
from flask_login import current_user

from . import main
from .. import login_manager
from ..models import User, Entry
from .forms import DatepickForm

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/', methods=["GET", "POST"])
@main.route('/index', methods=["GET", "POST"])
def index():
    hits = []
    sum = timedelta()
    datepickform = DatepickForm()
    is_logged_in = current_user.is_authenticated

    if is_logged_in:
        entries = Entry.return_from(current_user.id)

    else:
        entries = []

    if datepickform.validate_on_submit():
        month = datepickform.datepick.data.month
        year = datepickform.datepick.data.year
        for entry in entries:
            if month == entry.date.month and year == entry.date.year:
                hits.append(entry)
        entries = hits
    for entry in entries:
        sum += entry.time_worked()
    sum = float(sum.total_seconds()/3600)
    return render_template("index.html", entries=entries, form=datepickform, is_logged_in=is_logged_in, sum=sum)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@main.app_errorhandler(403)
def server_error(e):
    return render_template("403.html"), 403