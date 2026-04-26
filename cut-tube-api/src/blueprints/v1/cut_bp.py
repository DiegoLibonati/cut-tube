from flask import Blueprint

from src.controllers.cut_controller import alive, clip_video, download_clip, remove_clip

cut_bp = Blueprint("cut", __name__)

cut_bp.route("/alive", methods=["GET"])(alive)
cut_bp.route("/<filename>/clip", methods=["POST"])(clip_video)
cut_bp.route("/<filename>/download", methods=["GET"])(download_clip)
cut_bp.route("/<filename>", methods=["DELETE"])(remove_clip)
