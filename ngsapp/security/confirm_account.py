from uuid import UUID

from flask_restful.reqparse import RequestParser
from flask_restplus import Resource

from ngsapp.models import User
from ngsapp.security import auth


@auth.route('/confirm-account')
class ConfirmAccount(Resource):
    def post(self):
        parser = RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('token', type=str, required=True, location='args', help='Token is missing')
        args = parser.parse_args(strict=True)
        token = User.authenticate_token(args.token)
        if not token:
            return {'message': 'Token is invalid or has expired,please generate a new one'}, 400
        user = User.query.filter(User.uuid == UUID(token.get('id'))).first_or_404()
        if user.confirmed:
            return {'message': 'Your account is already confirmed'}, 200
        user.confirmed = True
        user.save()
        return {'message': 'your account has been successfully activated'}, 200
