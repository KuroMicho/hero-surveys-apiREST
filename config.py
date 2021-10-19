import os


DB_URL = f"postgresql+psycopg2://postgres:1234@localhost/hero_surveys"

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    
    # flasgger config
    from swagger import swagger_config
    SWAGGER = swagger_config

    @staticmethod
    def init_app(app):
        pass

    if os.environ.get('JWT_SECRET_KEY'):
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    else:
        JWT_SECRET_KEY = 'JWT_SECRET_KEY_ENV_VAR_NOT_SET'
        print('JWT_SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    HOST = 'localhost',  # Running on localhost
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS=False,

    @classmethod
    def init_app(cls, app):
        print('[Dev Config]THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')

