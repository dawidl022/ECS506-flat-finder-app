from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_uuid import FlaskUUID
from injector import Binder
from app.clients.ZooplaClient import ZooplaClient
from app.listings.models import Source
from app.listings.service import (
    GeocodingService, ListingsService, BaseListingsService)
from app.user.user_repository import InMemoryUserRepository
from app.user.user_service import BaseUserService, UserService, AdminService
from app.util.encoding import CamelCaseEncoder
from app.listings.repository import (
    InMemoryAccommodationListingsRepository, InMemoryPhotoRepository)
from config import Config


def register_common_blueprints(app: Flask) -> None:
    """
    Register blueprints common to both test and production setup
    """
    from app.listings import listings_bp
    app.register_blueprint(listings_bp)

    from app.user import users_bp
    app.register_blueprint(users_bp)

    from app.admins import admins_bp
    app.register_blueprint(admins_bp)


def initialise_common_extensions(app: Flask) -> None:
    """
    Initialise extensions common to both test and production setup
    """
    FlaskUUID(app)


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class())

    # Initialize Flask extensions
    CORS(app, resources={r"/api/*": {"origins": [Config().FRONTEND_URL]}})
    JWTManager(app)
    initialise_common_extensions(app)

    # Register blueprints
    register_common_blueprints(app)

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
        external_sources={
            Source.zoopla: ZooplaClient(Config().ZOOPLA_API_KEY)
        }
    )
    user_service = UserService(
        repo=InMemoryUserRepository(),
        listings_service=listing_service,
    )

    binder.bind(
        BaseListingsService, to=listing_service  # type: ignore[type-abstract]
    )
    binder.bind(
        BaseUserService, to=user_service  # type: ignore[type-abstract]
    )
    binder.bind(
        AdminService, to=user_service  # type: ignore[type-abstract]
    )
