from unittest.mock import patch
from flask_injector import FlaskInjector
from injector import Binder
import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app.listings.service import BaseListingsService
from app import initialise_common_extensions, register_common_blueprints
from app.user.user_service import BaseUserService
from tests.listings.test_routes import MockListingService
from tests.user.test_user_routes import MockUserService


@pytest.fixture(autouse=True)
def neuter_jwt():
    with patch("flask_jwt_extended.view_decorators.verify_jwt_in_request") as mock_get_jwt_identity:
        yield


@pytest.fixture(autouse=True)
def neuter_jwt_identity():
    with patch("flask_jwt_extended.utils.get_jwt") as mock_get_jwt_identity:
        mock_get_jwt_identity.return_value = {
            "sub": {"email": "unittest@user.com"}
        }
        yield


@pytest.fixture()
def app(listings_service: MockListingService, user_service: MockUserService
        ) -> Generator[Flask, None, None]:
    app = Flask(__name__)
    initialise_common_extensions(app)
    register_common_blueprints(app)

    app.config.update({
        "TESTING": True,
        'JWT_IDENTITY_CLAIM': 'sub'
    })

    # other setup can go here

    # Inject mock dependencies
    FlaskInjector(app=app, modules=[
        configure_mocks(listings_service, user_service)
    ])

    yield app

    # clean up / reset resources here


@pytest.fixture
def listings_service() -> MockListingService:
    return MockListingService()


@pytest.fixture
def user_service() -> MockUserService:
    return MockUserService()


def configure_mocks(listings_service: MockListingService, user_service: MockUserService):
    def wrapper(binder: Binder):

        binder.bind(
            BaseListingsService,  # type: ignore[type-abstract]
            to=listings_service
        )
        binder.bind(
            BaseUserService,  # type: ignore[type-abstract]
            to=user_service
        )

    return wrapper


@ pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@ pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
