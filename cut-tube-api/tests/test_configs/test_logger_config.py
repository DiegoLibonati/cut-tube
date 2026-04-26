import logging

import pytest

from src.configs.logger_config import setup_logger


@pytest.mark.unit
class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-instance")
        assert isinstance(logger, logging.Logger)

    def test_logger_name_matches_argument(self) -> None:
        name: str = "test-logger-name"
        logger: logging.Logger = setup_logger(name)
        assert logger.name == name

    def test_default_name_is_cut_tube_api(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "cut-tube-api"

    def test_has_stream_handler_after_setup(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-handler")
        handler_types: list[type] = [type(h) for h in logger.handlers]
        assert logging.StreamHandler in handler_types

    def test_idempotent_no_duplicate_handlers(self) -> None:
        name: str = "test-logger-idempotent"
        setup_logger(name)
        setup_logger(name)
        logger: logging.Logger = setup_logger(name)
        assert len(logger.handlers) == 1

    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-level")
        assert logger.level == logging.DEBUG
