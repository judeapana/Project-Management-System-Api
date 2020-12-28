import random

from flask import jsonify, url_for
from flask_bcrypt import generate_password_hash
from flask_restful.reqparse import RequestParser
from flask_restplus import Resource
from flask_restplus import inputs

from ngsapp.models import User
from ngsapp.security import auth
from ngsapp.tasks.mail import send_mail_rq


@auth.route('/email-check')
class EmailResource(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('email_address', required=True, location='json')
        args = parser.parse_args(strict=True)
        user = User.query.filter(User.email == args.email_address).first()
        if user:
            return {'status': True}, 400
        return {'status': False}, 200


@auth.route('/register')
class RegisterResource(Resource):
    def post(self):
        parser = RequestParser(bundle_errors=True)
        parser.add_argument('full_name', type=str, required=True, location='json')
        parser.add_argument('password', type=inputs.regex('[A-Za-z0-9@#$%^&+=]{8,}'), required=True, location='json',
                            help='Password must have a minimum of eight characters.')
        parser.add_argument('email_address', type=inputs.email(), required=True, location='json')
        args = parser.parse_args(strict=True)

        email = User.query.filter(User.email == args.email_address).first()
        if email:
            return {'message': 'Email address already exist'}, 400

        try:
            user = User()
            user.full_name = args.full_name
            user.email = args.email_address
            user.username = f'{args.full_name.replace(" ", "").lower()}{random.randint(1, 9999)}'
            user.password = generate_password_hash(args.password).decode()
            user.role = 'CLIENT'
            token = user.create_token()
            user.save()
            text = f"""Your Account has been created.
            Confirm Your Account By Clicking on this link.
            Link : <a href="{url_for('api.auth_confirm_account', token=token, _external=True)}"></a>
            """
            send_mail_rq.queue(user.email, text, 'Register')
            return {'message': 'Your account has been created, Check your email to confirm your account'}, 200
        except Exception as e:
            return jsonify(message=f'Unable to create account ::{e}'), 500
