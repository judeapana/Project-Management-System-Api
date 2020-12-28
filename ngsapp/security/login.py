from datetime import datetime

from flask import request, jsonify, make_response
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity, set_access_cookies, set_refresh_cookies
from flask_restplus import Resource, inputs
from flask_restplus.reqparse import RequestParser

from ngsapp.common.constants import LOGIN_NOTIFY
from ngsapp.models import User
from ngsapp.security import auth
from ngsapp.tasks.mail import send_mail_rq


@auth.route('/')
class Login(Resource):
    def post(self):
        parser = RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, location='json', help='username is required')
        parser.add_argument('password', type=str, required=True, location='json', help='password is required')
        parser.add_argument('rem', type=inputs.boolean, default=False, required=False, location='json',
                            help='rem is required')
        args = parser.parse_args(strict=True)
        user = User.query.filter((User.username == args.username) | (User.email == args.username)).first()
        if not user:
            return {'message': 'Incorrect username or password'}, 401
        else:
            if not check_password_hash(user.password, args.password):
                return {'message': 'Incorrect username or password'}, 401
            else:
                if not user.status:
                    return {'message': 'Your account is currently inactive'}, 401
                else:
                    send_mail_rq.queue(LOGIN_NOTIFY.format(name=user.full_name, app_name='Ngsapps', email=user.email,
                                                           time=str(datetime.utcnow()), ip=request.remote_addr,
                                                           user_agent=request.user_agent), [user.email],
                                       'Ngsapp Support')
                    # create JWT
                    access_token = create_access_token(identity=str(user.uuid))
                    refresh_token = create_refresh_token(identity=str(user.uuid))
                    resp = jsonify({'login': True, 'role': user.role})

                    set_access_cookies(resp, access_token)
                    set_refresh_cookies(resp, refresh_token)
                    resp.set_cookie('access_token_cookie', access_token)
                    # access_jti = get_jti(encoded_token=access_token)
                    # refresh_jti = get_jti(encoded_token=refresh_token)
                    # redis.set(access_jti, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
                    # redis.set(refresh_jti, 'false', current_app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.2)
                    return make_response(resp)
                    # return resp, 200
                    # return {'access_token': access_token, 'refresh_token': refresh_token,
                    #         'user': {'username': user.username, 'role': user.role}}, 200


@auth.route('/refresh')
class Refresh(Resource):
    method_decorators = [jwt_refresh_token_required]

    def post(self):
        parser = RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, location='json', help='username is required')
        parser.add_argument('password', type=str, required=True, location='json', help='password is required')
        args = parser.parse_args(strict=True)
        user = User.query.filter((User.username == args.username) | (User.email == args.username)).first()
        if not user:
            return {'message': 'Incorrect username or password'}, 401
        else:
            if not check_password_hash(user.password, args.password):
                return {'message': 'Incorrect username or password'}, 401
            else:
                if not user.status:
                    return {'message': 'Your account is currently inactive'}, 401
                else:
                    current_user = get_jwt_identity()
                    access_token = create_access_token(identity=current_user)
                    # access_jti = get_jti(encoded_token=access_token)
                    # redis.set(access_jti, 'false', current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
                    resp = jsonify({'login': True, 'role': user.role})
                    set_access_cookies(resp, access_token)
                    return resp, 200
                    # return {'token': {'access_token': access_token},
                    #         'user': {'username': user.username, 'role': user.role}}, 201
