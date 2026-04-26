from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytubefix.exceptions import VideoUnavailable

from src.services.video_tube_service import VideoTubeService


@pytest.fixture
def video_service() -> Generator[VideoTubeService, None, None]:
    with patch("src.services.video_tube_service.FileService.path_exists", return_value=True):
        svc: VideoTubeService = VideoTubeService(
            url="https://www.youtube.com/watch?v=test123",
            filename="test_clip",
            folder_download="/tmp/download",
            folder_clips="/tmp/clips",
        )
    yield svc


@pytest.mark.unit
class TestVideoTubeServiceProperties:
    def test_url_property(self, video_service: VideoTubeService) -> None:
        assert video_service.url == "https://www.youtube.com/watch?v=test123"

    def test_filename_property(self, video_service: VideoTubeService) -> None:
        assert video_service.filename == "test_clip"

    def test_name_is_none_initially(self, video_service: VideoTubeService) -> None:
        assert video_service.name is None

    def test_duration_is_zero_initially(self, video_service: VideoTubeService) -> None:
        assert video_service.duration == 0


@pytest.mark.unit
class TestGetVideoFromYoutube:
    def test_returns_false_for_non_youtube_url(self) -> None:
        with patch("src.services.video_tube_service.FileService.path_exists", return_value=True):
            svc: VideoTubeService = VideoTubeService(
                url="https://vimeo.com/video123",
                filename="clip",
                folder_download="/tmp/d",
                folder_clips="/tmp/c",
            )
        _, status = svc.get_video_from_youtube()
        assert status is False

    def test_returns_message_for_non_youtube_url(self) -> None:
        with patch("src.services.video_tube_service.FileService.path_exists", return_value=True):
            svc: VideoTubeService = VideoTubeService(
                url="https://vimeo.com/video123",
                filename="clip",
                folder_download="/tmp/d",
                folder_clips="/tmp/c",
            )
        message, _ = svc.get_video_from_youtube()
        assert "unavailable" in message.lower()

    def test_returns_false_for_http_url(self) -> None:
        with patch("src.services.video_tube_service.FileService.path_exists", return_value=True):
            svc: VideoTubeService = VideoTubeService(
                url="http://www.youtube.com/watch?v=abc",
                filename="clip",
                folder_download="/tmp/d",
                folder_clips="/tmp/c",
            )
        _, status = svc.get_video_from_youtube()
        assert status is False

    def test_returns_true_on_valid_youtube_url(self, video_service: VideoTubeService) -> None:
        mock_yt: MagicMock = MagicMock()
        mock_yt.streams = MagicMock()
        mock_yt.length = 120

        with patch("src.services.video_tube_service.YouTube", return_value=mock_yt):
            _, status = video_service.get_video_from_youtube()

        assert status is True

    def test_returns_correct_message_on_success(self, video_service: VideoTubeService) -> None:
        mock_yt: MagicMock = MagicMock()
        mock_yt.streams = MagicMock()
        mock_yt.length = 120

        with patch("src.services.video_tube_service.YouTube", return_value=mock_yt):
            message, _ = video_service.get_video_from_youtube()

        assert message == "Correct URL."

    def test_sets_duration_from_youtube_length(self, video_service: VideoTubeService) -> None:
        mock_yt: MagicMock = MagicMock()
        mock_yt.streams = MagicMock()
        mock_yt.length = 240

        with patch("src.services.video_tube_service.YouTube", return_value=mock_yt):
            video_service.get_video_from_youtube()

        assert video_service.duration == 240

    def test_returns_false_on_video_unavailable(self, video_service: VideoTubeService) -> None:
        with patch("src.services.video_tube_service.YouTube", side_effect=VideoUnavailable("test123")):
            _, status = video_service.get_video_from_youtube()
        assert status is False

    def test_returns_false_on_generic_exception(self, video_service: VideoTubeService) -> None:
        with patch("src.services.video_tube_service.YouTube", side_effect=RuntimeError("network error")):
            _, status = video_service.get_video_from_youtube()
        assert status is False


@pytest.mark.unit
class TestGetBetterStream:
    def test_raises_when_streams_is_none(self, video_service: VideoTubeService) -> None:
        with pytest.raises(ValueError, match="You must enter streams"):
            video_service.get_better_stream(streams=None)

    def test_raises_when_streams_is_empty_list(self, video_service: VideoTubeService) -> None:
        with pytest.raises(ValueError, match="You must enter streams"):
            video_service.get_better_stream(streams=[])

    def test_returns_best_stream(self, video_service: VideoTubeService) -> None:
        mock_stream: MagicMock = MagicMock()
        mock_streams: MagicMock = MagicMock()
        mock_streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value = mock_stream

        result = video_service.get_better_stream(streams=mock_streams)

        assert result == mock_stream

    def test_filters_by_progressive_and_mp4(self, video_service: VideoTubeService) -> None:
        mock_streams: MagicMock = MagicMock()
        mock_streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value = MagicMock()

        video_service.get_better_stream(streams=mock_streams)

        mock_streams.filter.assert_called_once_with(progressive=True, file_extension="mp4")

    def test_orders_by_resolution_desc(self, video_service: VideoTubeService) -> None:
        mock_streams: MagicMock = MagicMock()
        mock_streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value = MagicMock()

        video_service.get_better_stream(streams=mock_streams)

        mock_streams.filter.return_value.order_by.assert_called_once_with("resolution")


@pytest.mark.unit
class TestDownloadStream:
    def test_raises_when_stream_is_none(self, video_service: VideoTubeService) -> None:
        with pytest.raises(ValueError, match="No valid stream found"):
            video_service.download_stream()

    def test_sets_name_after_download(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()

        video_service.download_stream()

        assert video_service.name is not None
        assert video_service.name.endswith(".mp4")

    def test_calls_stream_download(self, video_service: VideoTubeService) -> None:
        mock_stream: MagicMock = MagicMock()
        video_service._VideoTubeService__stream = mock_stream

        video_service.download_stream()

        mock_stream.download.assert_called_once()

    def test_modifies_filename_to_include_uuid(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()
        original: str = video_service.filename

        video_service.download_stream()

        assert video_service.filename != original
        assert original in video_service.filename

    def test_stream_download_receives_output_path(self, video_service: VideoTubeService) -> None:
        mock_stream: MagicMock = MagicMock()
        video_service._VideoTubeService__stream = mock_stream

        video_service.download_stream()

        _, kwargs = mock_stream.download.call_args
        assert kwargs.get("output_path") == "/tmp/download"


@pytest.mark.unit
class TestGenerateClip:
    def test_raises_assertion_when_cannot_clip(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()

        with patch.object(video_service, "download_stream"):
            with pytest.raises(AssertionError, match="A clip still cannot be generated"):
                video_service.generate_clip("00:00:10", "00:00:20")

    def test_generates_clip_and_writes_file(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()
        video_service._VideoTubeService__duration = 100

        def set_can_clip() -> None:
            video_service._VideoTubeService__can_clip = True
            video_service._VideoTubeService__filename = "test_clip_uuid"

        mock_video: MagicMock = MagicMock()
        mock_clip: MagicMock = MagicMock()
        mock_video.subclipped.return_value = mock_clip

        with (
            patch.object(video_service, "download_stream", side_effect=set_can_clip),
            patch("src.services.video_tube_service.VideoFileClip", return_value=mock_video),
            patch("src.services.video_tube_service.FileService.remove_file"),
        ):
            video_service.generate_clip("00:00:10", "00:00:20")

        mock_clip.write_videofile.assert_called_once()

    def test_closes_clip_and_video_after_write(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()
        video_service._VideoTubeService__duration = 100

        def set_can_clip() -> None:
            video_service._VideoTubeService__can_clip = True
            video_service._VideoTubeService__filename = "test_clip_uuid"

        mock_video: MagicMock = MagicMock()
        mock_clip: MagicMock = MagicMock()
        mock_video.subclipped.return_value = mock_clip

        with (
            patch.object(video_service, "download_stream", side_effect=set_can_clip),
            patch("src.services.video_tube_service.VideoFileClip", return_value=mock_video),
            patch("src.services.video_tube_service.FileService.remove_file"),
        ):
            video_service.generate_clip("00:00:10", "00:00:20")

        mock_clip.close.assert_called_once()
        mock_video.close.assert_called_once()

    def test_removes_download_file_after_clip(self, video_service: VideoTubeService) -> None:
        video_service._VideoTubeService__stream = MagicMock()
        video_service._VideoTubeService__duration = 100

        def set_can_clip() -> None:
            video_service._VideoTubeService__can_clip = True
            video_service._VideoTubeService__filename = "test_clip_uuid"

        mock_video: MagicMock = MagicMock()
        mock_video.subclipped.return_value = MagicMock()

        with (
            patch.object(video_service, "download_stream", side_effect=set_can_clip),
            patch("src.services.video_tube_service.VideoFileClip", return_value=mock_video),
            patch("src.services.video_tube_service.FileService.remove_file") as mock_remove,
        ):
            video_service.generate_clip("00:00:10", "00:00:20")

        mock_remove.assert_called_once()


@pytest.mark.unit
class TestGenerateFolders:
    def test_creates_missing_folders(self) -> None:
        with (
            patch("src.services.video_tube_service.FileService.path_exists", return_value=False),
            patch("src.services.video_tube_service.FileService.make_dirs") as mock_makedirs,
        ):
            VideoTubeService(
                url="https://www.youtube.com/watch?v=test",
                filename="clip",
                folder_download="/tmp/missing_d",
                folder_clips="/tmp/missing_c",
            )
        assert mock_makedirs.call_count == 2

    def test_skips_existing_folders(self) -> None:
        with (
            patch("src.services.video_tube_service.FileService.path_exists", return_value=True),
            patch("src.services.video_tube_service.FileService.make_dirs") as mock_makedirs,
        ):
            VideoTubeService(
                url="https://www.youtube.com/watch?v=test",
                filename="clip",
                folder_download="/tmp/existing_d",
                folder_clips="/tmp/existing_c",
            )
        mock_makedirs.assert_not_called()
