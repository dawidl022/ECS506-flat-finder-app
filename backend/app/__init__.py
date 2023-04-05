from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from injector import Binder
from app.listings.service import (
    GeocodingService, ListingsService, BaseListingsService)
from app.util.encoding import CamelCaseEncoder
from app.listings.repository import (
    InMemoryAccommodationListingsRepository, InMemoryPhotoRepository)
from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class())

    # Initialize Flask extensions
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
    listing_service = ListingsService(
        accommodation_listing_repo=InMemoryAccommodationListingsRepository(),
        listing_photo_repo=InMemoryPhotoRepository(),
        geocoder=GeocodingService(),
    )

    binder.bind(
        BaseListingsService, to=listing_service  # type: ignore[type-abstract]
    )
