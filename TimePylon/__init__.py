from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect

from .config import config_by_name

db = SQLAlchemy()
#csrf = CSRFProtect()

# auth config
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


#enable DebugToolbar
toolbar = DebugToolbarExtension()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
#    csrf.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    from .entries import entries as entry_blueprint
    app.register_blueprint(entry_blueprint, url_prefix="/entries")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app



