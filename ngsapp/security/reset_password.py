from uuid import UUID

from flask_bcrypt import generate_password_hash
from flask_restful.reqparse import RequestParser
from flask_restplus import Resource
from flask_restplus import inputs
from werkzeug.security import safe_str_cmp

from ngsapp.models import User
from ngsapp.security import auth


@auth.route('/reset-pwd')
class ResetPassword(Resource):
    parser = RequestParser(bundle_errors=True)

    def get(self):
        ResetPassword.parser.add_argument('token', type=str, required=True, location='args',
                                          help='Token is missing')
        args = ResetPassword.parser.parse_args(strict=True)
        token = User.authenticate_token(args.token)
        if not token:
            return {'message': 'Token is invalid or has expired', "other": 'Please regenerate token'}, 400
        return {'message': 'Token is valid'}

    def put(self):
        xparser = RequestParser(bundle_errors=True)
        xparser.add_argument('token', type=str, required=True, location='args',
                                          help='Token is missing')
        xparser.add_argument('new_pwd', type=inputs.regex('[A-Za-z0-9@#$%^&+=]{8,}'),
                                          required=True, location='json',
                                          help='Password must have a minimum of eight characters.')
        xparser.add_argument('confirm_pwd', type=inputs.regex('[A-Za-z0-9@#$%^&+=]{8,}'),
                                          required=True, location='json',
                                          help='Password must have a minimum of eight characters.')
        args = xparser.parse_args(strict=True)

        token = User.authenticate_token(args.token)
        if not token:
            return {'message': 'Token is invalid or has expired', "other": 'Please regenerate token'}
        try:
            if not safe_str_cmp(args.confirm_pwd, args.new_pwd):
                return {"message": 'passwords dont match'}
            user = User.query.filter(User.uuid == UUID(token.get('id'))).first()
            user.password = generate_password_hash(args.new_pwd).decode()
            user.save()
            return {'message': 'Your password has been updated successfully'}
        except Exception:
            return {'message': 'Something went wrong', 'other': 'unable to update password'}
