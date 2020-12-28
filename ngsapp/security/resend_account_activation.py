from flask import jsonify, url_for
from flask_restful.reqparse import RequestParser
from flask_restplus import Resource
from flask_restplus import inputs

from ngsapp.common.constants import CONFIRM_ACC
from ngsapp.models import User
from ngsapp.security import auth
from ngsapp.tasks.mail import send_mail_rq


@auth.route('/resend-acc')
class ResendAccountActivation(Resource):
    def post(self):
        parser = RequestParser(bundle_errors=True)
        parser.add_argument('email_address', type=inputs.email(), required=True, location='json')
        args = parser.parse_args(strict=True)
        user = User.query.filter(User.email == args.email_address).first()
        if not user:
            return jsonify(message='Please account is not found')
        if user.status:
            return jsonify(message='Your dont have access to this function')
        token = user.create_token()
        url = url_for('api.auth_confirm_account', token=token, _external=True)
        send_mail_rq.queue(CONFIRM_ACC.format(url=url, name=user.full_name), [user.email], 'Resend Account Activation')
        return jsonify(message='Account confirmation has been sent')
