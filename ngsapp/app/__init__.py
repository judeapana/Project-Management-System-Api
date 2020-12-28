import datetime

from flask import Blueprint
from flask_jwt_extended import get_raw_jwt

app = Blueprint('app', __name__, template_folder='templates', url_prefix='/app')

# from . import auth


# @app.context_processor
# def csrf():
#     return dict(csrf=(get_raw_jwt() or {}).get("csrf"))
#
#
# @app.context_processor
# def datetimt():
#     return dict(datetime=datetime)
