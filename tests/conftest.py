import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.services.wechat import VerifiedPhoneNumber, WeChatCredentialError
from tests.support import sample_engine


class FakeWeChatMiniProgramClient:
    def __init__(self):
        self.login_codes = []
        self.phone_codes = []
        self.phone = VerifiedPhoneNumber(
            canonical="+8613800138000",
            lookup_values=("+8613800138000", "13800138000", "8613800138000"),
            normalized_lookup_values=("8613800138000", "13800138000"),
        )

    def exchange_login_code(self, login_code):
        self.login_codes.append(login_code)
        if login_code == "expired":
            raise WeChatCredentialError("expired")
        return "test-openid"

    def get_phone_number(self, phone_code):
        self.phone_codes.append(phone_code)
        if phone_code == "expired":
            raise WeChatCredentialError("expired")
        return self.phone


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-not-for-production-123",
        static_dir=tmp_path / "static",
        uploads_dir=tmp_path / "static" / "uploads",
        audio_enabled=False,
        wechat_miniprogram_app_id="wx-test-app",
        wechat_miniprogram_app_secret="test-mini-program-secret",
    )
    app = create_app(settings, sample_engine())
    app.state.wechat_miniprogram = FakeWeChatMiniProgramClient()
    with TestClient(app) as client:
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
