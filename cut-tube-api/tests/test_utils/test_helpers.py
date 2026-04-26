import pytest

from src.utils.helpers import get_portion_seconds, time_to_seconds


@pytest.mark.unit
class TestTimeToSeconds:
    def test_converts_seconds_only(self) -> None:
        assert time_to_seconds("00:00:10") == 10

    def test_converts_minutes_only(self) -> None:
        assert time_to_seconds("00:01:00") == 60

    def test_converts_hours_only(self) -> None:
        assert time_to_seconds("01:00:00") == 3600

    def test_converts_combined_time(self) -> None:
        assert time_to_seconds("01:01:01") == 3661

    def test_converts_zero(self) -> None:
        assert time_to_seconds("00:00:00") == 0

    def test_converts_max_seconds_in_minute(self) -> None:
        assert time_to_seconds("00:00:59") == 59

    def test_converts_two_hours(self) -> None:
        assert time_to_seconds("02:00:00") == 7200

    def test_returns_integer(self) -> None:
        result: int = time_to_seconds("00:01:30")
        assert isinstance(result, int)


@pytest.mark.unit
class TestGetPortionSeconds:
    def test_returns_correct_portion_for_half(self) -> None:
        result: int = get_portion_seconds(100, "00:00:50")
        assert result == 50

    def test_returns_zero_for_start(self) -> None:
        result: int = get_portion_seconds(3600, "00:00:00")
        assert result == 0

    def test_returns_full_duration_at_end(self) -> None:
        result: int = get_portion_seconds(3600, "01:00:00")
        assert result == 3600

    def test_returns_integer(self) -> None:
        result: int = get_portion_seconds(120, "00:00:30")
        assert isinstance(result, int)

    def test_truncates_to_integer(self) -> None:
        result: int = get_portion_seconds(100, "00:00:10")
        assert result == 10

    def test_proportional_calculation(self) -> None:
        result: int = get_portion_seconds(200, "00:00:50")
        assert result == 50
