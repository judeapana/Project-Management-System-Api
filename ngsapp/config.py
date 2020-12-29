from datetime import timedelta


class Config:
    APP_NAME = 'Your application name'
    APP_LESS_NAME = 'short name or url for your application'
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'a9a3c143b9dac091f39ce0d89ba0607ad31a64249582ec0ba0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/-your database name-'
    MAIL_SERVER = 'your mail server domain name'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'your mail server username'
    MAIL_PASSWORD = 'your mail server password'
    MAIL_DEFAULT_SENDER = 'noreply.yourdomain@yourdomain.com'
    PAGINATE_PAGE_SIZE = 10
    PAGINATE_RESOURCE_LINKS_ENABLED = True
    JWT_SECRET_KEY = 'a9a3c143b9dac091f39ce0d89ba0607ad31a64249582ec0ba'
    # JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=5)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_CSRF_CHECK_FORM = False


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    JWT_COOKIE_SECURE = True
