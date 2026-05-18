import pytest
from flask import Flask


@pytest.mark.unit
class TestRegisterRoutes:
    def test_health_route_is_registered(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/health/" in rules

    def test_health_route_allows_get(self, app: Flask) -> None:
        rules: dict[str, object] = {str(r): r for r in app.url_map.iter_rules()}
        assert "GET" in rules["/api/v1/health/"].methods

    def test_alive_route_is_registered(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/cut/alive" in rules

    def test_clip_route_is_registered(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/cut/<filename>/clip" in rules

    def test_download_route_is_registered(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/cut/<filename>/download" in rules

    def test_delete_route_is_registered(self, app: Flask) -> None:
        rules: list[str] = [str(rule) for rule in app.url_map.iter_rules()]
        assert "/api/v1/cut/<filename>" in rules

    def test_alive_route_allows_get(self, app: Flask) -> None:
        rules: dict[str, object] = {str(r): r for r in app.url_map.iter_rules()}
        assert "GET" in rules["/api/v1/cut/alive"].methods

    def test_clip_route_allows_post(self, app: Flask) -> None:
        rules: dict[str, object] = {str(r): r for r in app.url_map.iter_rules()}
        assert "POST" in rules["/api/v1/cut/<filename>/clip"].methods

    def test_download_route_allows_get(self, app: Flask) -> None:
        rules: dict[str, object] = {str(r): r for r in app.url_map.iter_rules()}
        assert "GET" in rules["/api/v1/cut/<filename>/download"].methods

    def test_delete_route_allows_delete(self, app: Flask) -> None:
        rules: dict[str, object] = {str(r): r for r in app.url_map.iter_rules()}
        assert "DELETE" in rules["/api/v1/cut/<filename>"].methods

    def test_all_cut_routes_share_v1_prefix(self, app: Flask) -> None:
        cut_rules: list[str] = [str(r) for r in app.url_map.iter_rules() if "cut" in str(r)]
        assert all(r.startswith("/api/v1/cut") for r in cut_rules)

    def test_all_health_routes_share_v1_prefix(self, app: Flask) -> None:
        health_rules: list[str] = [str(r) for r in app.url_map.iter_rules() if str(r).startswith("/api/v1/health")]
        assert len(health_rules) > 0
        assert all(r.startswith("/api/v1/health") for r in health_rules)
