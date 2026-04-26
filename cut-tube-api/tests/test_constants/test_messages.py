import pytest

from src.constants.messages import (
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_INTERNAL_SERVER,
    MESSAGE_ERROR_PYDANTIC,
    MESSAGE_ERROR_VIDEO_TUBE_SERVICE,
    MESSAGE_NOT_FOUND_PATH,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_SUCCESS_CUT_VIDEO,
    MESSAGE_SUCCESS_DELETE_CLIP,
)


@pytest.mark.unit
class TestMessages:
    def test_success_cut_video(self) -> None:
        assert MESSAGE_SUCCESS_CUT_VIDEO == "Video cutted."

    def test_success_delete_clip(self) -> None:
        assert MESSAGE_SUCCESS_DELETE_CLIP == "Clip deleted."

    def test_error_internal_server(self) -> None:
        assert MESSAGE_ERROR_INTERNAL_SERVER == "Internal server error."

    def test_error_pydantic(self) -> None:
        assert MESSAGE_ERROR_PYDANTIC == "Pydantic error."

    def test_error_video_tube_service(self) -> None:
        assert MESSAGE_ERROR_VIDEO_TUBE_SERVICE == "VideoTubeService error."

    def test_not_valid_fields(self) -> None:
        assert MESSAGE_NOT_VALID_FIELDS == "Not valid fields."

    def test_not_found_path(self) -> None:
        assert MESSAGE_NOT_FOUND_PATH == "Not found path."

    def test_error_generic_contains_placeholder(self) -> None:
        assert "{e}" in MESSAGE_ERROR_GENERIC

    def test_all_messages_are_strings(self) -> None:
        messages: list[str] = [
            MESSAGE_SUCCESS_CUT_VIDEO,
            MESSAGE_SUCCESS_DELETE_CLIP,
            MESSAGE_ERROR_INTERNAL_SERVER,
            MESSAGE_ERROR_PYDANTIC,
            MESSAGE_ERROR_VIDEO_TUBE_SERVICE,
            MESSAGE_NOT_VALID_FIELDS,
            MESSAGE_NOT_FOUND_PATH,
            MESSAGE_ERROR_GENERIC,
        ]
        assert all(isinstance(m, str) for m in messages)
