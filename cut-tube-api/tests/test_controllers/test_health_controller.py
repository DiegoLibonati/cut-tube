from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.controllers.health_controller import health, ready


@pytest.mark.integration
class TestHealthEndpoint:
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        assert response.status_code == 200

    def test_response_contains_success_health_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_HEALTH"

    def test_response_contains_health_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "The application is healthy."

    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        assert response.content_type.startswith("application/json")


@pytest.mark.unit
class TestHealthFunction:
    def test_returns_tuple(self, app: Flask) -> None:
        with app.test_request_context():
            result = health()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_status_200(self, app: Flask) -> None:
        with app.test_request_context():
            _, status_code = health()
        assert status_code == 200

    def test_response_json_body(self, app: Flask) -> None:
        with app.test_request_context():
            response, _ = health()
        body: dict[str, Any] = response.get_json()
        assert body["code"] == "SUCCESS_HEALTH"
        assert body["message"] == "The application is healthy."


@pytest.mark.unit
class TestReadyFunction:
    def test_returns_tuple(self, app: Flask) -> None:
        with app.test_request_context():
            result = ready()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_status_200(self, app: Flask) -> None:
        with app.test_request_context():
            _, status_code = ready()
        assert status_code == 200

    def test_response_contains_ready_code(self, app: Flask) -> None:
        with app.test_request_context():
            response, _ = ready()
        body: dict[str, Any] = response.get_json()
        assert body["code"] == "SUCCESS_READY"

    def test_response_contains_ready_message(self, app: Flask) -> None:
        with app.test_request_context():
            response, _ = ready()
        body: dict[str, Any] = response.get_json()
        assert body["message"] == "The application is ready to serve requests."
