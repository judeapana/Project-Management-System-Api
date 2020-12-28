import datetime

from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')
from . import forgot_pwd, login, register, reset_pwd, resend_cnf, change_email, confirm_acc


@auth.before_request
def check_auth():
    pass


@auth.context_processor
def datetimt():
    return dict(datetime=datetime)
