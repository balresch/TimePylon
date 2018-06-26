from flask import url_for
from flask_testing import TestCase
from flask_login import current_user
from datetime import date, time

import TimePylon
from TimePylon.models import User, Entry

class TimePylonTestCase(TestCase):

    def create_app(self):
        return TimePylon.create_app("test")

    def setUp(self):
        self.db = TimePylon.db
        self.db.create_all()
        self.client = self.app.test_client()

        u = User(username="test", email="test@example.com", password="test")
        self.db.session.add(u)
        self.db.session.commit()
        entry = Entry(date=date(2018, 7, 12), start=time(hour=14, minute=20), end=time(hour=18, minute=45), pause="50", comment="Testkommentar", user_id=u.id)
        self.db.session.add(entry)
        self.db.session.commit()

        self.client.post(url_for("auth.login"),
                         data = dict(username="test", password="test"))

    def tearDown(self):
        TimePylon.db.session.remove()
        TimePylon.db.drop_all()

    def test_edit_entry(self):
#        assert current_user.is_authenticated
        response = self.client.post(
            url_for("entries.edit_entry", entry_id=1),
            data=dict(end=time(hour=18, minute=50)),
            follow_redirects=True
        )

        assert response.status_code == 200
        entry = Entry.query.first()
#        assert entry.end.minute == 50