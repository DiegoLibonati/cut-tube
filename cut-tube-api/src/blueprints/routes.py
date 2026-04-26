from flask import Flask

from src.blueprints.v1.cut_bp import cut_bp


def register_routes(app: Flask) -> None:
    prefix = "/api/v1"

    app.register_blueprint(cut_bp, url_prefix=f"{prefix}/cut")
