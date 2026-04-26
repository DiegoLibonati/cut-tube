import logging
import os
import uuid

from moviepy import VideoFileClip
from pytubefix import Stream, YouTube, exceptions, streams

from src.constants.paths import FOLDER_CLIPS, FOLDER_DOWNLOAD
from src.constants.vars import CLIP_EXTENSION
from src.services.file_service import FileService
from src.utils.helpers import get_portion_seconds

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class VideoTubeService:
    def __init__(
        self,
        url: str,
        filename: str,
        folder_download: str = FOLDER_DOWNLOAD,
        folder_clips: str = FOLDER_CLIPS,
        extension: str = CLIP_EXTENSION,
    ) -> None:
        self.__url = url
        self.__filename: str = filename
        self.__extension: str = extension
        self.__name: str = None

        self.__folder_download: str = folder_download
        self.__folder_clips: str = folder_clips

        self.__duration: int = 0
        self.__stream: Stream = None
        self.__can_clip: bool = False

        self._generate_folders()

    @property
    def url(self) -> str:
        return self.__url

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def name(self) -> str:
        return self.__name

    @property
    def duration(self) -> int:
        return self.__duration

    def get_video_from_youtube(self) -> tuple:
        try:
            if not self.url.startswith("https://www.youtube.com/watch?"):
                return f"Video {self.url} is unavailable.", False

            video = YouTube(url=self.url, on_progress_callback=self.__on_progress)

            if not video:
                return (
                    "You need a pytube.YouTube object before getting the best stream.",
                    False,
                )

            self.__stream = self.get_better_stream(streams=video.streams)
            self.__duration = video.length

            return "Correct URL.", True
        except exceptions.VideoUnavailable:
            return f"Video {self.url} is unavaialable", False
        except Exception as e:
            return e, False

    def get_better_stream(self, streams: streams) -> Stream:
        if not streams:
            raise ValueError("You must enter streams to get the best one.")

        return streams.filter(progressive=True, file_extension=self.__extension).order_by("resolution").desc().first()

    def download_stream(self) -> None:
        if not self.filename:
            raise ValueError("You must enter a valid file name.")

        self.__filename = f"{self.filename}_{uuid.uuid4()}"
        self.__name = f"{self.__filename}.{self.__extension}"

        if not self.__stream:
            raise ValueError("No valid stream found to download.")

        self.__stream.download(
            output_path=self.__folder_download,
            filename=f"{self.filename}.{self.__extension}",
        )

    def generate_clip(self, start_time: str, end_time: str) -> None:
        self.download_stream()

        if not self.__can_clip:
            raise AssertionError("A clip still cannot be generated.")

        if not self.filename:
            raise ValueError("You must enter a valid file name.")

        path_download = os.path.join(self.__folder_download, f"{self.filename}.{self.__extension}")
        path_clip = os.path.join(self.__folder_clips, f"{self.filename}.{self.__extension}")

        video = VideoFileClip(path_download)

        clip = video.subclipped(
            get_portion_seconds(self.duration, start_time),
            get_portion_seconds(self.duration, end_time),
        )
        clip.write_videofile(path_clip)

        clip.close()
        video.close()

        FileService.remove_file(path_download)

        self.__can_clip = False

    def __on_progress(self, stream: streams.Stream, chunk: bytes, bytes_remaining: int) -> None:
        if not bytes_remaining:
            self.__can_clip = True

    def _generate_folders(self) -> None:
        folders = [self.__folder_download, self.__folder_clips]

        for folder in folders:
            if not FileService.path_exists(folder):
                FileService.make_dirs(folder)

        logging.info("FOLDERS GENERATED")


def init() -> None:
    filename_clip = "pepe"
    start_clip = "00:00:10"
    end_clip = "00:00:20"
    link_clip = "https://www.youtube.com/watch?v=joHCGlzxi8U&ab_channel=FeidVEVO"

    video = VideoTubeService(url=link_clip, filename=filename_clip)

    _, status = video.get_video_from_youtube()

    if not status:
        return logging.info("Error 1")

    video.generate_clip(start_time=start_clip, end_time=end_clip)


if __name__ == "__main__":
    init()
