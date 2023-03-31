from flask_injector import FlaskInjector
from injector import Binder
import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app import create_app
from app.listings.service import ListingsService


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
        ListingsService, to=MockListingService()
    )


class MockListingService(ListingsService):
    def search_accommodation_listings(self):
        return []


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
