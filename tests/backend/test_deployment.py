import pytest
from fastapi.testclient import TestClient

from app.main import _cors_origins, app


def test_cors_middleware_allows_local_development_origin():
    response = TestClient(app).options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_origins_include_local_and_configured_frontend(monkeypatch):
    monkeypatch.delenv("FRONTEND_ORIGIN", raising=False)
    assert _cors_origins() == ["http://localhost:5173", "http://127.0.0.1:5173"]

    monkeypatch.setenv("FRONTEND_ORIGIN", "https://afficionado-intelligence.vercel.app/")
    origins = _cors_origins()
    assert origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://afficionado-intelligence.vercel.app",
    ]
    assert "*" not in origins


def test_cors_origin_rejects_non_origin_url(monkeypatch):
    monkeypatch.setenv("FRONTEND_ORIGIN", "https://example.com/app")
    with pytest.raises(ValueError, match="without a path"):
        _cors_origins()
