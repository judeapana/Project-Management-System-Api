from flask import jsonify, url_for
from flask_restful.reqparse import RequestParser
from flask_restplus import Resource
from flask_restplus import inputs

from ngsapp.common.constants import FORGOT_PWD
from ngsapp.models import User
from ngsapp.security import auth
from ngsapp.tasks.mail import send_mail_rq


@auth.route('/forgot-pwd')
class ForgotPassword(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('email_address', type=inputs.email(), required=True, location='json')
        args = parser.parse_args(strict=True)
        user = User.query.filter(User.email == args.email_address).first()
        if not user:
            return {'message': 'Sorry, your email was not found', 'other': 'Check and try again'}, 400
        token = user.create_token()
        send_mail_rq.queue(
            FORGOT_PWD.format(url=url_for('api.auth_reset_password', token=token, _external=True), name=user.full_name),
            [user.email], 'Forgot Password')
        print(token)
        return jsonify(message='A reset link has been sent to your email')
