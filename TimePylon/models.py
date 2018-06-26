from datetime import datetime, timedelta, time, date
from TimePylon import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import desc


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    pause = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        pass
#        return "<Eintrag - {}:{}, {}:{}, {}:{}, {}:{}, {}:{}>".format()

    @staticmethod
    def return_all():
        return Entry.query.order_by(desc(Entry.date)).all()

    @staticmethod
    def return_from(user_id):
        return Entry.query.filter_by(user_id=user_id).order_by(Entry.date).all()

    def time_worked(self):
        time1 = datetime.combine(date.today(), self.start)
        time2 = datetime.combine(date.today(), self.end)
        pause = timedelta(minutes=int(self.pause))
        result = time2 - time1 - pause
        return result


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    entries_of_user = db.relationship("Entry", backref="user", lazy="dynamic")
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("password: write-only field")


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()


    def __repr__(self):
        return "<User %r>" % self.username
