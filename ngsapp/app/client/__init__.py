from flask import Blueprint

client = Blueprint('client', __name__, template_folder='template', url_prefix='/client')
from . import dashboard
