from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from flask import Response
from flask.testing import FlaskClient


@pytest.mark.integration
class TestAlive:
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/cut/alive")
        assert response.status_code == 200

    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/cut/alive")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    def test_response_contains_version(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/cut/alive")
        data: dict[str, Any] = response.get_json()
        assert "version_bp" in data

    def test_response_contains_author(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/cut/alive")
        data: dict[str, Any] = response.get_json()
        assert data["author"] == "Diego Libonati"

    def test_response_contains_name_bp(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/cut/alive")
        data: dict[str, Any] = response.get_json()
        assert data["name_bp"] == "Cut"


@pytest.mark.integration
class TestClipVideo:
    def test_returns_200_on_success(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.VideoTubeService") as mock_cls:
            mock_svc: MagicMock = MagicMock()
            mock_cls.return_value = mock_svc
            mock_svc.get_video_from_youtube.return_value = ("Correct URL.", True)
            mock_svc.name = "test_video"
            mock_svc.filename = "test_clip"

            response = client.post(
                "/api/v1/cut/test_clip/clip",
                json={"url": "https://www.youtube.com/watch?v=abc", "start": "00:00:10", "end": "00:00:20"},
            )

        assert response.status_code == 200

    def test_response_contains_success_code(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.VideoTubeService") as mock_cls:
            mock_svc: MagicMock = MagicMock()
            mock_cls.return_value = mock_svc
            mock_svc.get_video_from_youtube.return_value = ("Correct URL.", True)
            mock_svc.name = "test_video"
            mock_svc.filename = "test_clip"

            response = client.post(
                "/api/v1/cut/test_clip/clip",
                json={"url": "https://www.youtube.com/watch?v=abc", "start": "00:00:10", "end": "00:00:20"},
            )

        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_CUT_VIDEO"

    def test_response_contains_data_with_name_and_filename(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.VideoTubeService") as mock_cls:
            mock_svc: MagicMock = MagicMock()
            mock_cls.return_value = mock_svc
            mock_svc.get_video_from_youtube.return_value = ("Correct URL.", True)
            mock_svc.name = "test_video"
            mock_svc.filename = "test_clip"

            response = client.post(
                "/api/v1/cut/test_clip/clip",
                json={"url": "https://www.youtube.com/watch?v=abc", "start": "00:00:10", "end": "00:00:20"},
            )

        data: dict[str, Any] = response.get_json()
        assert "name" in data["data"]
        assert "filename" in data["data"]

    def test_returns_409_when_video_load_fails(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.VideoTubeService") as mock_cls:
            mock_svc: MagicMock = MagicMock()
            mock_cls.return_value = mock_svc
            mock_svc.get_video_from_youtube.return_value = ("Video unavailable.", False)

            response = client.post(
                "/api/v1/cut/test_clip/clip",
                json={"url": "https://www.youtube.com/watch?v=abc", "start": "00:00:10", "end": "00:00:20"},
            )

        assert response.status_code == 409

    def test_returns_400_on_missing_body_fields(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/cut/test_clip/clip", json={})
        assert response.status_code == 400

    def test_returns_400_on_empty_url(self, client: FlaskClient) -> None:
        response = client.post(
            "/api/v1/cut/test_clip/clip",
            json={"url": "", "start": "00:00:10", "end": "00:00:20"},
        )
        assert response.status_code == 400

    def test_calls_generate_clip_with_start_and_end(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.VideoTubeService") as mock_cls:
            mock_svc: MagicMock = MagicMock()
            mock_cls.return_value = mock_svc
            mock_svc.get_video_from_youtube.return_value = ("Correct URL.", True)
            mock_svc.name = "v"
            mock_svc.filename = "f"

            client.post(
                "/api/v1/cut/test_clip/clip",
                json={"url": "https://www.youtube.com/watch?v=abc", "start": "00:00:05", "end": "00:00:15"},
            )

        mock_svc.generate_clip.assert_called_once_with(start_time="00:00:05", end_time="00:00:15")


@pytest.mark.integration
class TestDownloadClip:
    def test_returns_404_when_file_not_found(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.FileService.path_exists", return_value=False):
            response = client.get("/api/v1/cut/nonexistent/download")
        assert response.status_code == 404

    def test_returns_404_response_code_field(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.FileService.path_exists", return_value=False):
            response = client.get("/api/v1/cut/nonexistent/download")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "NOT_FOUND_PATH"

    def test_returns_200_when_file_exists(self, client: FlaskClient) -> None:
        with (
            patch("src.controllers.cut_controller.FileService.path_exists", return_value=True),
            patch("src.controllers.cut_controller.send_file") as mock_send,
        ):
            mock_send.return_value = Response("file_content", status=200, mimetype="video/mp4")
            response = client.get("/api/v1/cut/test_clip/download")
        assert response.status_code == 200

    def test_send_file_called_with_mp4_mimetype(self, client: FlaskClient) -> None:
        with (
            patch("src.controllers.cut_controller.FileService.path_exists", return_value=True),
            patch("src.controllers.cut_controller.send_file") as mock_send,
        ):
            mock_send.return_value = Response("file_content", status=200, mimetype="video/mp4")
            client.get("/api/v1/cut/test_clip/download")

        _, kwargs = mock_send.call_args
        assert kwargs.get("mimetype") == "video/mp4" or mock_send.call_args[0]


@pytest.mark.integration
class TestRemoveClip:
    def test_returns_404_when_file_not_found(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.FileService.path_exists", return_value=False):
            response = client.delete("/api/v1/cut/nonexistent")
        assert response.status_code == 404

    def test_returns_200_when_file_exists(self, client: FlaskClient) -> None:
        with (
            patch("src.controllers.cut_controller.FileService.path_exists", return_value=True),
            patch("src.controllers.cut_controller.FileService.remove_file"),
        ):
            response = client.delete("/api/v1/cut/test_clip")
        assert response.status_code == 200

    def test_response_contains_success_code(self, client: FlaskClient) -> None:
        with (
            patch("src.controllers.cut_controller.FileService.path_exists", return_value=True),
            patch("src.controllers.cut_controller.FileService.remove_file"),
        ):
            response = client.delete("/api/v1/cut/test_clip")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "SUCCESS_DELETE_CLIP"

    def test_remove_file_is_called(self, client: FlaskClient) -> None:
        with (
            patch("src.controllers.cut_controller.FileService.path_exists", return_value=True),
            patch("src.controllers.cut_controller.FileService.remove_file") as mock_remove,
        ):
            client.delete("/api/v1/cut/test_clip")
        mock_remove.assert_called_once()

    def test_returns_404_response_code_field(self, client: FlaskClient) -> None:
        with patch("src.controllers.cut_controller.FileService.path_exists", return_value=False):
            response = client.delete("/api/v1/cut/nonexistent")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "NOT_FOUND_PATH"
