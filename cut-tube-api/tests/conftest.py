from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture(scope="session")
def app() -> Generator[Flask, None, None]:
    flask_app = create_app("testing")
    yield flask_app


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()
