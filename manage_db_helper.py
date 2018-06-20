"""
> python manage_db_helper.py db init
    initializes flask_migrate (already done)
> python manage_db_helper.py db migrate -m "migrate name"
    adds a migration and creates the scripts needed
> python manage_db_helper.py db upgrade
    run the scripts to update to latest migration
> python manage_db_helper.py db upgrade --tag "migration name"
    run the scripts to update to mentioned migration
> python manage_db_helper.py db downgrade --tag "migration name"
    run the scripts to downgrade to mentioned migration
"""


from TimePylon import create_app, db
from TimePylon.models import User
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from os import getenv


app = create_app(getenv("TIMEPYLON_ENV") or "dev")

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)




@manager.command
def addtestdata():
#    db.create_all()
    db.session.add(User(id=0, username="balresch", email="balresch@gmail.com", password="test"))
    db.session.add(User(id=1, username="kimi", email="kim.thiesen92@gmail.com", password="test2"))
    db.session.commit()
    print("added test data")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data?"):
        print(db)
        db.drop_all()
        print("dropped the database")


if __name__ == "__main__":
    manager.run()
