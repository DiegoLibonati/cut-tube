import pytest
from flask import Blueprint

from src.blueprints.v1.cut_bp import cut_bp


@pytest.mark.unit
class TestCutBlueprint:
    def test_blueprint_is_flask_blueprint(self) -> None:
        assert isinstance(cut_bp, Blueprint)

    def test_blueprint_name_is_cut(self) -> None:
        assert cut_bp.name == "cut"

    def test_blueprint_has_deferred_functions(self) -> None:
        assert len(cut_bp.deferred_functions) > 0
