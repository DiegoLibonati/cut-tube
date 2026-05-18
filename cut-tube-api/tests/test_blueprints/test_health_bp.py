import pytest
from flask import Blueprint

from src.blueprints.v1.health_bp import health_bp


@pytest.mark.unit
class TestHealthBlueprint:
    def test_blueprint_is_flask_blueprint(self) -> None:
        assert isinstance(health_bp, Blueprint)

    def test_blueprint_name_is_health(self) -> None:
        assert health_bp.name == "health"

    def test_blueprint_has_deferred_functions(self) -> None:
        assert len(health_bp.deferred_functions) > 0
