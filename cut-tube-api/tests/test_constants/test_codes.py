import pytest

from src.constants.codes import (
    CODE_ERROR_GENERIC,
    CODE_ERROR_INTERNAL_SERVER,
    CODE_ERROR_PYDANTIC,
    CODE_ERROR_VIDEO_TUBE_SERVICE,
    CODE_NOT_FOUND_PATH,
    CODE_NOT_VALID_FIELDS,
    CODE_SUCCESS_CUT_VIDEO,
    CODE_SUCCESS_DELETE_CLIP,
)


@pytest.mark.unit
class TestCodes:
    def test_success_cut_video(self) -> None:
        assert CODE_SUCCESS_CUT_VIDEO == "SUCCESS_CUT_VIDEO"

    def test_success_delete_clip(self) -> None:
        assert CODE_SUCCESS_DELETE_CLIP == "SUCCESS_DELETE_CLIP"

    def test_error_internal_server(self) -> None:
        assert CODE_ERROR_INTERNAL_SERVER == "ERROR_INTERNAL_SERVER"

    def test_error_pydantic(self) -> None:
        assert CODE_ERROR_PYDANTIC == "ERROR_PYDANTIC"

    def test_error_generic(self) -> None:
        assert CODE_ERROR_GENERIC == "ERROR_GENERIC"

    def test_error_video_tube_service(self) -> None:
        assert CODE_ERROR_VIDEO_TUBE_SERVICE == "ERROR_VIDEO_TUBE_SERVICE"

    def test_not_valid_fields(self) -> None:
        assert CODE_NOT_VALID_FIELDS == "NOT_VALID_FIELDS"

    def test_not_found_path(self) -> None:
        assert CODE_NOT_FOUND_PATH == "NOT_FOUND_PATH"

    def test_all_codes_are_strings(self) -> None:
        codes: list[str] = [
            CODE_SUCCESS_CUT_VIDEO,
            CODE_SUCCESS_DELETE_CLIP,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_GENERIC,
            CODE_ERROR_VIDEO_TUBE_SERVICE,
            CODE_NOT_VALID_FIELDS,
            CODE_NOT_FOUND_PATH,
        ]
        assert all(isinstance(c, str) for c in codes)
