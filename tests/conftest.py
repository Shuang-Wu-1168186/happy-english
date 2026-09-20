import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from tests.support import sample_engine


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-not-for-production-123",
        static_dir=tmp_path / "static",
        uploads_dir=tmp_path / "static" / "uploads",
        audio_enabled=False,
    )
    with TestClient(create_app(settings, sample_engine())) as client:
        yield client


def sign_in(client, username="admin_test"):
    token = client.get("/api/auth/session").json()["csrf_token"]
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": "Testing123!"},
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 200
    return {"X-CSRF-Token": response.json()["csrf_token"]}
