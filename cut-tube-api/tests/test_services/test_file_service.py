from unittest.mock import patch

import pytest

from src.services.file_service import FileService


@pytest.mark.unit
class TestPathExists:
    def test_returns_true_when_path_exists(self) -> None:
        with patch("src.services.file_service.os.path.exists", return_value=True):
            result: bool = FileService.path_exists("/some/path")
        assert result is True

    def test_returns_false_when_path_missing(self) -> None:
        with patch("src.services.file_service.os.path.exists", return_value=False):
            result: bool = FileService.path_exists("/missing/path")
        assert result is False

    def test_calls_os_path_exists_with_given_path(self) -> None:
        with patch("src.services.file_service.os.path.exists") as mock_exists:
            mock_exists.return_value = True
            FileService.path_exists("/target/path")
        mock_exists.assert_called_once_with("/target/path")


@pytest.mark.unit
class TestRemoveFile:
    def test_calls_os_remove_with_given_path(self) -> None:
        with patch("src.services.file_service.os.remove") as mock_remove:
            FileService.remove_file("/some/file.mp4")
        mock_remove.assert_called_once_with("/some/file.mp4")

    def test_propagates_os_error_when_file_missing(self) -> None:
        with (
            patch("src.services.file_service.os.remove", side_effect=FileNotFoundError("not found")),
            pytest.raises(FileNotFoundError),
        ):
            FileService.remove_file("/missing/file.mp4")


@pytest.mark.unit
class TestMakeDirs:
    def test_calls_os_makedirs_with_given_path(self) -> None:
        with patch("src.services.file_service.os.makedirs") as mock_makedirs:
            FileService.make_dirs("/new/folder")
        mock_makedirs.assert_called_once_with("/new/folder", exist_ok=True)

    def test_passes_exist_ok_true_by_default(self) -> None:
        with patch("src.services.file_service.os.makedirs") as mock_makedirs:
            mock_makedirs.return_value = None
            FileService.make_dirs("/folder")
        _, kwargs = mock_makedirs.call_args
        assert kwargs.get("exist_ok") is True

    def test_passes_custom_exist_ok_false(self) -> None:
        with patch("src.services.file_service.os.makedirs") as mock_makedirs:
            mock_makedirs.return_value = None
            FileService.make_dirs("/folder", exist_ok=False)
        _, kwargs = mock_makedirs.call_args
        assert kwargs.get("exist_ok") is False

    def test_returns_none(self) -> None:
        with patch("src.services.file_service.os.makedirs", return_value=None) as _mock_makedirs:
            result: None = FileService.make_dirs("/folder")
        assert result is None
