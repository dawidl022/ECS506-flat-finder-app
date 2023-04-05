from flask_injector import FlaskInjector
from injector import Binder
import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app import create_app
from app.listings.service import BaseListingsService
from tests.listings.test_routes import MockListingService


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
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


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
