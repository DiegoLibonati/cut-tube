from typing import Any

import pytest
from flask import Flask

from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


@pytest.mark.unit
class TestBaseAPIError:
    def test_default_status_code(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.status_code == 500

    def test_default_message(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert isinstance(error.message, str)
        assert len(error.message) > 0

    def test_custom_message(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom error")
        assert error.message == "custom error"

    def test_custom_code(self) -> None:
        error: BaseAPIError = BaseAPIError(code="CUSTOM_CODE")
        assert error.code == "CUSTOM_CODE"

    def test_custom_status_code(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)
        assert error.status_code == 418

    def test_to_dict_contains_code_and_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="ERR", message="msg")
        result: dict[str, Any] = error.to_dict()
        assert result["code"] == "ERR"
        assert result["message"] == "msg"

    def test_to_dict_excludes_empty_payload(self) -> None:
        error: BaseAPIError = BaseAPIError()
        result: dict[str, Any] = error.to_dict()
        assert "payload" not in result

    def test_to_dict_includes_payload_when_provided(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"detail": "info"})
        result: dict[str, Any] = error.to_dict()
        assert "payload" in result
        assert result["payload"]["detail"] == "info"

    def test_flask_response_returns_tuple_with_status(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(status_code=500)
            response, status_code = error.flask_response()
        assert status_code == 500

    def test_flask_response_status_matches_error(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(status_code=422)
            _, status_code = error.flask_response()
        assert status_code == 422


@pytest.mark.unit
class TestExceptionSubclasses:
    def test_validation_error_status_400(self) -> None:
        assert ValidationAPIError.status_code == 400

    def test_authentication_error_status_401(self) -> None:
        assert AuthenticationAPIError.status_code == 401

    def test_not_found_error_status_404(self) -> None:
        assert NotFoundAPIError.status_code == 404

    def test_conflict_error_status_409(self) -> None:
        assert ConflictAPIError.status_code == 409

    def test_business_error_status_422(self) -> None:
        assert BusinessAPIError.status_code == 422

    def test_internal_error_status_500(self) -> None:
        assert InternalAPIError.status_code == 500

    def test_all_subclasses_inherit_base(self) -> None:
        subclasses: list[type] = [
            ValidationAPIError,
            AuthenticationAPIError,
            NotFoundAPIError,
            ConflictAPIError,
            BusinessAPIError,
            InternalAPIError,
        ]
        assert all(issubclass(cls, BaseAPIError) for cls in subclasses)

    def test_validation_error_is_exception(self) -> None:
        error: ValidationAPIError = ValidationAPIError(code="V", message="v")
        assert isinstance(error, Exception)

    def test_not_found_error_custom_message(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError(code="NF", message="not found here")
        assert error.message == "not found here"
        assert error.status_code == 404
