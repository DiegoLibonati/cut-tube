import os

from flask import Response, jsonify, request, send_file

from src.constants.codes import (
    CODE_ERROR_VIDEO_TUBE_SERVICE,
    CODE_NOT_FOUND_PATH,
    CODE_NOT_VALID_FIELDS,
    CODE_SUCCESS_CUT_VIDEO,
    CODE_SUCCESS_DELETE_CLIP,
)
from src.constants.messages import (
    MESSAGE_NOT_FOUND_PATH,
    MESSAGE_NOT_VALID_FIELDS,
    MESSAGE_SUCCESS_CUT_VIDEO,
    MESSAGE_SUCCESS_DELETE_CLIP,
)
from src.constants.paths import (
    FOLDER_CLIPS,
    FOLDER_CLIPS_DOCKER,
    FOLDER_DOWNLOAD_DOCKER,
)
from src.constants.vars import CLIP_EXTENSION
from src.models.clip_model import ClipModel
from src.services.file_service import FileService
from src.services.video_tube_service import VideoTubeService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError, ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


@exceptions_handler
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Cut",
    }

    return jsonify(response), 200


@exceptions_handler
def clip_video(filename: str) -> Response:
    body = request.get_json()

    clip = ClipModel(filename=filename, **body)

    video_tube_service = VideoTubeService(
        url=clip.url,
        filename=clip.filename,
        folder_clips=FOLDER_CLIPS_DOCKER,
        folder_download=FOLDER_DOWNLOAD_DOCKER,
    )

    message, load_video = video_tube_service.get_video_from_youtube()

    if not load_video:
        raise ConflictAPIError(code=CODE_ERROR_VIDEO_TUBE_SERVICE, message=message)

    video_tube_service.generate_clip(
        start_time=clip.start,
        end_time=clip.end,
    )

    response = {
        "code": CODE_SUCCESS_CUT_VIDEO,
        "message": MESSAGE_SUCCESS_CUT_VIDEO,
        "data": {
            "name": video_tube_service.name,
            "filename": video_tube_service.filename,
        },
    }

    return jsonify(response), 200


@exceptions_handler
def download_clip(filename: str) -> Response:
    if not filename:
        raise ValidationAPIError(code=CODE_NOT_VALID_FIELDS, message=MESSAGE_NOT_VALID_FIELDS)

    name = f"{filename}.{CLIP_EXTENSION}"
    docker_path = os.path.join(FOLDER_CLIPS_DOCKER, name)
    fs_path = os.path.join(FOLDER_CLIPS, name)

    if not FileService.path_exists(fs_path) and not FileService.path_exists(docker_path):
        raise NotFoundAPIError(code=CODE_NOT_FOUND_PATH, message=MESSAGE_NOT_FOUND_PATH)

    file_path = docker_path if FileService.path_exists(docker_path) else os.path.join(FOLDER_CLIPS, name)

    return send_file(
        file_path,
        mimetype=f"video/{CLIP_EXTENSION}",
        as_attachment=True,
        download_name=name,
    )


@exceptions_handler
def remove_clip(filename: str) -> Response:
    if not filename:
        raise ValidationAPIError(code=CODE_NOT_VALID_FIELDS, message=MESSAGE_NOT_VALID_FIELDS)

    name = f"{filename}.{CLIP_EXTENSION}"
    docker_path = os.path.join(FOLDER_CLIPS_DOCKER, name)
    fs_path = os.path.join(FOLDER_CLIPS, name)

    if not FileService.path_exists(fs_path) and not FileService.path_exists(docker_path):
        raise NotFoundAPIError(code=CODE_NOT_FOUND_PATH, message=MESSAGE_NOT_FOUND_PATH)

    file_path = docker_path if FileService.path_exists(docker_path) else os.path.join(FOLDER_CLIPS, name)

    FileService.remove_file(file_path)

    response = {
        "code": CODE_SUCCESS_DELETE_CLIP,
        "message": MESSAGE_SUCCESS_DELETE_CLIP,
    }

    return jsonify(response), 200
