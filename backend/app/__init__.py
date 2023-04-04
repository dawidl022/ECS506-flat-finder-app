from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder
from app.listings.service import GeocodingService, ListingsService
from app.util.encoding import CamelCaseEncoder
from app.listings.repository import (
    InMemoryAccommodationListingsRepository, InMemoryPhotoRepository)
from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_encoder = CamelCaseEncoder

    # Initialize Flask extensions here

    # Register blueprints
    from app.listings import listings_bp
    app.register_blueprint(listings_bp)

    # Initialize Flask-Injector. This needs to be run *after* you attached all
    # views, handlers, context processors and template globals.
    FlaskInjector(app=app, modules=[configure_dependencies])

    return app


def configure_dependencies(binder: Binder) -> None:
    binder.bind(
        ListingsService, to=ListingsService(
            accommodation_listing_repo=InMemoryAccommodationListingsRepository(),
            listing_photo_repo=InMemoryPhotoRepository(),
            geocoder=GeocodingService(),
        )
    )
