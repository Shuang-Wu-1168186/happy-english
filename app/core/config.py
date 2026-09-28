from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    app_env: str = "development"
    secret_key: str = Field(min_length=32)
    database_url: str = "mysql+pymysql://happyenglish@127.0.0.1:3306/happy_english?charset=utf8mb4"
    cookie_secure: bool = False
    session_seconds: int = Field(default=43200, ge=60)
    audio_enabled: bool = False
    wechat_miniprogram_app_id: str = ""
    wechat_miniprogram_app_secret: str = ""
    wechat_request_timeout_seconds: float = Field(default=10, ge=1, le=60)
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    static_dir: Path = ROOT / "data" / "static"
    uploads_dir: Path = ROOT / "data" / "static" / "uploads"

    @model_validator(mode="after")
    def production_security(self):
        if self.app_env == "production":
            if not self.cookie_secure or self.secret_key.startswith("replace-"):
                raise ValueError("Production requires COOKIE_SECURE=true and a random SECRET_KEY.")
        return self
