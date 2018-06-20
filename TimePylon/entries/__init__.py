from flask import Blueprint

entries = Blueprint("entries", __name__)

from . import views
