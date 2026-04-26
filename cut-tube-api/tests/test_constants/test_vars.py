import pytest

from src.constants.vars import CLIP_EXTENSION


@pytest.mark.unit
class TestVars:
    def test_clip_extension_is_mp4(self) -> None:
        assert CLIP_EXTENSION == "mp4"

    def test_clip_extension_is_string(self) -> None:
        assert isinstance(CLIP_EXTENSION, str)

    def test_clip_extension_has_no_dot(self) -> None:
        assert not CLIP_EXTENSION.startswith(".")
