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

    def test_port_is_integer(self) -> None:
        assert isinstance(DefaultConfig.PORT, int)

    def test_max_content_length_is_integer(self) -> None:
        assert isinstance(DefaultConfig.MAX_CONTENT_LENGTH, int)

    def test_tz_fallback_is_buenos_aires(self) -> None:
        expected: str = os.getenv("TZ", "America/Argentina/Buenos_Aires")
        assert expected == DefaultConfig.TZ

    def test_work_dir_fallback_is_home_app(self) -> None:
        expected: str = os.getenv("WORK_DIR", "/home/app")
        assert expected == DefaultConfig.WORK_DIR

    def test_host_fallback_is_zero_zero_zero_zero(self) -> None:
        expected: str = os.getenv("HOST", "0.0.0.0")
        assert expected == DefaultConfig.HOST

    def test_port_reads_env_variable(self) -> None:
        expected: int = int(os.getenv("PORT", "5000"))
        assert expected == DefaultConfig.PORT

    def test_max_content_length_default_is_one_megabyte(self) -> None:
        expected: int = int(os.getenv("MAX_CONTENT_LENGTH", str(1 * 1024 * 1024)))
        assert expected == DefaultConfig.MAX_CONTENT_LENGTH

    def test_max_content_length_is_positive(self) -> None:
        assert DefaultConfig.MAX_CONTENT_LENGTH > 0

    def test_port_is_positive(self) -> None:
        assert DefaultConfig.PORT > 0
