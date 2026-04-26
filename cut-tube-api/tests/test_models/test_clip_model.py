import pytest
from pydantic import ValidationError

from src.models.clip_model import ClipModel


@pytest.mark.unit
class TestClipModelValid:
    def test_creates_model_with_valid_fields(self) -> None:
        clip: ClipModel = ClipModel(
            url="https://www.youtube.com/watch?v=abc",
            start="00:00:10",
            end="00:00:20",
            filename="my_clip",
        )
        assert clip.url == "https://www.youtube.com/watch?v=abc"
        assert clip.start == "00:00:10"
        assert clip.end == "00:00:20"
        assert clip.filename == "my_clip"

    def test_strips_whitespace_from_url(self) -> None:
        clip: ClipModel = ClipModel(
            url="  https://www.youtube.com/watch?v=abc  ",
            start="00:00:10",
            end="00:00:20",
            filename="clip",
        )
        assert clip.url == "https://www.youtube.com/watch?v=abc"

    def test_strips_whitespace_from_start(self) -> None:
        clip: ClipModel = ClipModel(
            url="https://www.youtube.com/watch?v=abc",
            start="  00:00:10  ",
            end="00:00:20",
            filename="clip",
        )
        assert clip.start == "00:00:10"

    def test_strips_whitespace_from_end(self) -> None:
        clip: ClipModel = ClipModel(
            url="https://www.youtube.com/watch?v=abc",
            start="00:00:10",
            end="  00:00:20  ",
            filename="clip",
        )
        assert clip.end == "00:00:20"

    def test_strips_whitespace_from_filename(self) -> None:
        clip: ClipModel = ClipModel(
            url="https://www.youtube.com/watch?v=abc",
            start="00:00:10",
            end="00:00:20",
            filename="  my_clip  ",
        )
        assert clip.filename == "my_clip"


@pytest.mark.unit
class TestClipModelInvalid:
    def test_raises_on_missing_url(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(start="00:00:10", end="00:00:20", filename="clip")

    def test_raises_on_missing_start(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", end="00:00:20", filename="clip")

    def test_raises_on_missing_end(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", start="00:00:10", filename="clip")

    def test_raises_on_missing_filename(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", start="00:00:10", end="00:00:20")

    def test_raises_on_empty_url(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="", start="00:00:10", end="00:00:20", filename="clip")

    def test_raises_on_whitespace_only_url(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="   ", start="00:00:10", end="00:00:20", filename="clip")

    def test_raises_on_empty_start(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", start="", end="00:00:20", filename="clip")

    def test_raises_on_empty_end(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", start="00:00:10", end="", filename="clip")

    def test_raises_on_empty_filename(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel(url="https://www.youtube.com/watch?v=abc", start="00:00:10", end="00:00:20", filename="")

    def test_raises_on_all_missing_fields(self) -> None:
        with pytest.raises(ValidationError):
            ClipModel()
