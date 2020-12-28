from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates', url_prefix='/')

from ngsapp.app.main import terms,index
