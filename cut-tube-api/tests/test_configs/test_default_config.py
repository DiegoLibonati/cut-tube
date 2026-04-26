import os

import pytest

from src.configs.default_config import DefaultConfig


@pytest.mark.unit
class TestDefaultConfig:
    def test_debug_is_false_by_default(self) -> None:
        assert DefaultConfig.DEBUG is False

    def test_testing_is_false_by_default(self) -> None:
        assert DefaultConfig.TESTING is False

    def test_host_is_string(self) -> None:
        assert isinstance(DefaultConfig.HOST, str)

    def test_tz_is_string(self) -> None:
        assert isinstance(DefaultConfig.TZ, str)

    def test_work_dir_is_string(self) -> None:
        assert isinstance(DefaultConfig.WORK_DIR, str)

    def test_tz_fallback_is_buenos_aires(self) -> None:
        expected: str = os.getenv("TZ", "America/Argentina/Buenos_Aires")
        assert DefaultConfig.TZ == expected

    def test_work_dir_fallback_is_home_app(self) -> None:
        expected: str = os.getenv("WORK_DIR", "/home/app")
        assert DefaultConfig.WORK_DIR == expected
