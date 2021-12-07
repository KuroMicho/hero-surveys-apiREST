import os
from datetime import timedelta
from flask import Flask, redirect, jsonify
from flask.helpers import make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended.utils import unset_access_cookies, unset_jwt_cookies
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from swagger import swagger_config, template
from src.constants.http_status_codes import HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
# from config import config as Config
from src.resources.routes import init_api
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")

cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
api = Api()


def create_app():
    app = Flask(__name__)

    app.config.from_object(env_config)
    app.config.from_mapping(
            JWT_TOKEN_LOCATION=['headers'],
            CORS_HEADERS = "Content-Type",
            # JWT_SESSION_COOKIE=True,
            # JWT_ACCESS_COOKIE_PATH='/',
            # JWT_REFRESH_COOKIE_PATH='/',
            # JWT_COOKIE_SAMESITE = 'None',
            # JWT_COOKIE_SECURE = True,
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
            JWT_COOKIE_CSRF_PROTECT=False,  # Change in production to True
            JWT_CSRF_CHECK_FORM=True,
    )

    # db.app = app
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app,  resources={r"/*": {"origins": "*", "Access-Control-Allow-Origin": "*"}}, supports_credentials=True)
    Swagger(app, config=swagger_config, template=template, parse=True)
    jwt = JWTManager(app)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    # @app.after_request
    # def middleware_for_response(response):
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     return response

    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        # No auth header
        # return redirect(app.config['BASE_URL'] + '/', 302)
        return {
            "message": "No auth header"
        }, HTTP_302_FOUND

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        # Invalid Fresh/Non-Fresh Access token in auth header
        # resp = make_response(redirect(app.config['BASE_URL'] + '/'))
        resp = make_response(jsonify({
            "message": "Invalid Fresh/Non-Fresh Access token in auth header"
        }), HTTP_302_FOUND)
        # unset_jwt_cookies(resp)
        return resp, 302

    @jwt.expired_token_loader
    def expired_token_callback(self, callback):
        # Expired auth header
        resp = make_response(
            redirect('localhost:5000/author/refresh'))
        # unset_access_cookies(resp)
        return resp, 302

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return {"error": "Page not Found"}, HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return {"error": "Something went wrong"}, HTTP_500_INTERNAL_SERVER_ERROR

    return app


init_api(api)
