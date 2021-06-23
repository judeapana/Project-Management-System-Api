from dotenv import load_dotenv
import datetime
from uuid import UUID

from flask import Flask

load_dotenv()
from ngsapp.config import DevelopmentConfig
from ngsapp.ext import cors, db, pagination, bcrypt, migrate, rq, ma, mail, jwt, redis
from ngsapp.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    pagination.init_app(app, db)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    app.register_blueprint(bapi)
    redis.init_app(app)
    #app.register_blueprint(application)
    #app.register_blueprint(main)
    #app.register_blueprint(client)
    #app.register_blueprint(auth)
    #app.register_blueprint(admin)

    @jwt.user_claims_loader
    def claim(identity):
        user = User.query.filter(User.uuid == identity).first()
        if user is None:
            return {}
        return {'role': user.role, 'email': user.email}

    @jwt.user_loader_callback_loader
    def load_user(identity):
        return User.query.filter(User.uuid == UUID(identity)).one()

    @app.context_processor
    def me_app():
        return dict(app_fullname=app.config.get('APP_NAME'), app_name=app.config.get('APP_LESS_NAME'))

    @app.context_processor
    def datetimt():
        return dict(datetime=datetime)



    # @jwt.token_in_blacklist_loader
    # def blacklist(decrypted_token):
    #     jti = decrypted_token['jti']
    #     entry = redis.get(jti)
    #     try:
    #         if entry is None:
    #             return True
    #         return entry.decode() == 'true'
    #     except:
    #         return True

    # with app.app_con
    # text():
    #     urlvars = False  # Build query strings in URLs
    #     swagger = True  # Export Swagger specifications
    #     data = api.as_postman(urlvars=urlvars, swagger=swagger)
    #     file = open('file.json', '+w')
    #     file.write(json.dumps(data))

    return app


from ngsapp.api.apiv1 import bapi
