from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from injector import Binder
from app.listings.service import (
    GeocodingService, ListingsService, BaseListingsService)
from app.user.user_repository import InMemoryUserRepository
from app.user.user_service import BaseUserService, UserService
from app.util.encoding import CamelCaseEncoder
from app.listings.repository import (
    InMemoryAccommodationListingsRepository, InMemoryPhotoRepository)
from config import Config


def register_blueprints(app: Flask) -> None:
    from app.listings import listings_bp
    app.register_blueprint(listings_bp)


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class())

    # Initialize Flask extensions
    CORS(app, resources={r"/api/*": {"origins": [Config().FRONTEND_URL]}})
    JWTManager(app)

    # Register blueprints
    register_blueprints(app)

    from app.auth.google import auth_bp
    app.register_blueprint(auth_bp)

    # Initialize Flask-Injector. This needs to be run *after* you attached all
    # views, handlers, context processors and template globals.
    FlaskInjector(app=app, modules=[configure_dependencies])

    return app


def configure_dependencies(binder: Binder) -> None:
    listing_service = ListingsService(
        accommodation_listing_repo=InMemoryAccommodationListingsRepository(),
        listing_photo_repo=InMemoryPhotoRepository(),
        geocoder=GeocodingService(),
    )
    user_service = UserService(
        repo=InMemoryUserRepository()
    )

    binder.bind(
        BaseListingsService, to=listing_service  # type: ignore[type-abstract]
    )
    binder.bind(
        BaseUserService, to=user_service  # type: ignore[type-abstract]
    )
