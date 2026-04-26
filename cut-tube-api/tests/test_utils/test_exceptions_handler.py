import pytest
from pydantic import BaseModel, ValidationError

from src.utils.exceptions import ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


def _make_pydantic_validation_error() -> ValidationError:
    class _Model(BaseModel):
        field: str

    try:
        _Model()
    except ValidationError as exc:
        return exc
    raise RuntimeError("Expected ValidationError was not raised")


@pytest.mark.unit
class TestExceptionsHandler:
    def test_returns_value_on_success(self) -> None:
        @exceptions_handler
        def fn() -> str:
            return "ok"

        result: str = fn()
        assert result == "ok"

    def test_returns_none_on_success(self) -> None:
        @exceptions_handler
        def fn() -> None:
            return None

        result: None = fn()
        assert result is None

    def test_passes_args_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(x: int, y: int) -> int:
            return x + y

        result: int = fn(2, 3)
        assert result == 5

    def test_passes_kwargs_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(name: str = "default") -> str:
            return name

        result: str = fn(name="custom")
        assert result == "custom"

    def test_converts_pydantic_validation_error_to_api_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise _make_pydantic_validation_error()

        with pytest.raises(ValidationAPIError):
            fn()

    def test_raised_validation_api_error_has_pydantic_code(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise _make_pydantic_validation_error()

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        assert exc_info.value.code == "ERROR_PYDANTIC"

    def test_raised_validation_api_error_has_details_in_payload(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise _make_pydantic_validation_error()

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        assert "details" in exc_info.value.payload

    def test_does_not_catch_value_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise ValueError("some error")

        with pytest.raises(ValueError):
            fn()

    def test_does_not_catch_runtime_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise RuntimeError("runtime")

        with pytest.raises(RuntimeError):
            fn()

    def test_preserves_original_function_name(self) -> None:
        @exceptions_handler
        def my_named_func() -> None:
            pass

        assert my_named_func.__name__ == "my_named_func"
