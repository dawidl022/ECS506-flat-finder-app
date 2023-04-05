from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from injector import Binder
from app.listings.service import ListingsService
from app.util.encoding import CamelCaseEncoder
from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class())

    # Initialize Flask extensions
    CORS(app, resources={r"/api/*": {"origins": [Config().FRONTEND_URL]}})
    JWTManager(app)

    # Register blueprints
    from app.listings import listings_bp
    app.register_blueprint(listings_bp)
    listings_bp.json_encoder = CamelCaseEncoder

    from app.auth.google import auth_bp
    app.register_blueprint(auth_bp)

    # Initialize Flask-Injector. This needs to be run *after* you attached all
    # views, handlers, context processors and template globals.
    FlaskInjector(app=app, modules=[configure_dependencies])

    return app


def configure_dependencies(binder: Binder) -> None:
    binder.bind(
        ListingsService, to=ListingsService()
    )
