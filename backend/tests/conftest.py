from unittest.mock import patch
from flask_injector import FlaskInjector
from injector import Binder
import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app.listings.service import BaseListingsService
from app import register_blueprints
from tests.listings.test_routes import MockListingService


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
def app() -> Generator[Flask, None, None]:
    app = Flask(__name__)
    register_blueprints(app)

    app.config.update({
        "TESTING": True,
        'JWT_IDENTITY_CLAIM': 'sub'
    })

    # other setup can go here

    # Inject mock dependencies
    FlaskInjector(app=app, modules=[configure_mocks])

    yield app

    # clean up / reset resources here


def configure_mocks(binder: Binder):
    binder.bind(
        BaseListingsService,  # type: ignore[type-abstract]
        to=MockListingService()
    )


@ pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@ pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
