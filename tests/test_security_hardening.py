import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.config import Settings
from app.core.security import COOKIE, SESSION_HEADER
from app.main import create_app
from tests.conftest import sign_in
from tests.support import sample_engine


def production_settings(**overrides):
    values = {
        "_env_file": None,
        "app_env": "production",
        "secret_key": "production-test-secret-key-not-for-production-123",
        "cookie_secure": True,
        "cors_origins": ["https://www.example.test"],
        "trusted_hosts": ["testserver"],
        "log_console": False,
    }
    values.update(overrides)
    return Settings(**values)


def test_production_settings_require_hardened_transport_configuration():
    with pytest.raises(ValidationError, match="COOKIE_SECURE"):
        production_settings(cookie_secure=False)
    with pytest.raises(ValidationError, match="CORS"):
        production_settings(cors_origins=["http://www.example.test"])
    with pytest.raises(ValidationError, match="TRUSTED_HOSTS"):
        production_settings(trusted_hosts=["*"])
    with pytest.raises(ValidationError, match="documentation"):
        production_settings(api_docs_enabled=True)


def test_production_disables_docs_rejects_unknown_hosts_and_sets_security_headers(tmp_path):
    settings = production_settings(
        static_dir=tmp_path / "static",
        uploads_dir=tmp_path / "static" / "uploads",
        log_dir=tmp_path / "logs",
    )
    with TestClient(create_app(settings, sample_engine())) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert response.headers["permissions-policy"] == "camera=(), geolocation=(), microphone=(self), payment=()"
        assert response.headers["content-security-policy"] == (
            "base-uri 'self'; frame-ancestors 'none'; object-src 'none'; form-action 'self'"
        )
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/api/health", headers={"Host": "untrusted.example.test"}).status_code == 400


def test_logout_revokes_a_copied_session_header(client):
    headers = sign_in(client)
    copied_session = client.cookies.get(COOKIE)

    response = client.post(
        "/api/auth/logout",
        headers={**headers, SESSION_HEADER: copied_session},
    )

    assert response.status_code == 200
    client.cookies.clear()
    assert client.get("/api/modules", headers={SESSION_HEADER: copied_session}).status_code == 401
