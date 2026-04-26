import pytest

from src.constants.paths import (
    ASSETS_DIR,
    BASE_DIR,
    FOLDER_CLIPS,
    FOLDER_CLIPS_DOCKER,
    FOLDER_DOWNLOAD,
    FOLDER_DOWNLOAD_DOCKER,
)


@pytest.mark.unit
class TestPaths:
    def test_base_dir_is_string(self) -> None:
        assert isinstance(str(BASE_DIR), str)

    def test_assets_dir_contains_assets(self) -> None:
        assert "assets" in ASSETS_DIR

    def test_folder_download_contains_download(self) -> None:
        assert "download" in FOLDER_DOWNLOAD

    def test_folder_clips_contains_clips(self) -> None:
        assert "clips" in FOLDER_CLIPS

    def test_folder_download_docker_contains_download(self) -> None:
        assert "download" in FOLDER_DOWNLOAD_DOCKER

    def test_folder_clips_docker_contains_clips(self) -> None:
        assert "clips" in FOLDER_CLIPS_DOCKER

    def test_folder_download_docker_contains_assets(self) -> None:
        assert "assets" in FOLDER_DOWNLOAD_DOCKER

    def test_folder_clips_docker_contains_assets(self) -> None:
        assert "assets" in FOLDER_CLIPS_DOCKER

    def test_all_paths_are_strings(self) -> None:
        paths: list[str] = [
            ASSETS_DIR,
            FOLDER_DOWNLOAD,
            FOLDER_CLIPS,
            FOLDER_DOWNLOAD_DOCKER,
            FOLDER_CLIPS_DOCKER,
        ]
        assert all(isinstance(p, str) for p in paths)
