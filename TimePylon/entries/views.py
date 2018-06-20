from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from datetime import datetime

from . import entries
from .. import db
from .forms import EntryForm
from ..models import Entry



@entries.route('/add', methods=["GET", "POST"])
@login_required
def add():
    entryform = EntryForm()
    if entryform.validate_on_submit():
        date = entryform.date.data
        start = datetime.strptime(entryform.start._value(), "%H:%M").time()
        end = datetime.strptime(entryform.end._value(), "%H:%M").time()
        pause = entryform.pause.data
        comment = entryform.comment.data
        entry = Entry(date=date, start=start, end=end, pause=pause, comment=comment, user_id=current_user.get_id())
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("addoredit.html", form=entryform)


@entries.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if current_user.id != entry.user_id:
        abort(403)
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("addoredit.html", form=form, title="Eintrag anpassen")


@entries.route("/delete/<int:entry_id>", methods=["GET", "POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if current_user.id != entry.user_id:
        abort(403)
    if request.method == "POST":
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("confirmdelete.html", entry=entry, title="Eintrag löschen")
