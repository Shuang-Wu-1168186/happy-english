from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    app_env: str = "development"
    secret_key: str = Field(min_length=32)
    # Defaults to a domain-separated derivation from SECRET_KEY. Set this to a
    # dedicated random value before rotating identifier tokens independently.
    external_id_secret: str = ""
    external_id_previous_secrets: list[str] = Field(default_factory=list)
    database_url: str = "mysql+pymysql://happyenglish@127.0.0.1:3306/happy_english?charset=utf8mb4"
    cookie_secure: bool = False
    # Browser sessions remain shorter by default; the Android app keeps its
    # signed session for a week so users are not forced to log in frequently.
    session_seconds: int = Field(default=43200, ge=60)
    app_session_seconds: int = Field(default=7 * 24 * 60 * 60, ge=60)
    audio_enabled: bool = False
    wechat_miniprogram_app_id: str = ""
    wechat_miniprogram_app_secret: str = ""
    wechat_request_timeout_seconds: float = Field(default=10, ge=1, le=60)
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    trusted_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "10.0.2.2", "testserver"]
    )
    # None keeps documentation enabled during development and disabled in production.
    api_docs_enabled: bool | None = None
    static_dir: Path = ROOT / "data" / "static"
    uploads_dir: Path = ROOT / "data" / "static" / "uploads"
    log_dir: Path = ROOT / "logs"
    log_level: str = "INFO"
    log_max_bytes: int = Field(default=10 * 1024 * 1024, ge=1024)
    log_backup_count: int = Field(default=5, ge=1, le=100)
    log_console: bool = True
    request_slow_ms: float = Field(default=1000, ge=0)

    @field_validator("log_level")
    @classmethod
    def valid_log_level(cls, value):
        level = value.strip().upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL.")
        return level

    @field_validator("app_env")
    @classmethod
    def valid_app_env(cls, value):
        environment = value.strip().lower()
        if environment not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production.")
        return environment

    @property
    def log_file(self) -> Path:
        return self.log_dir / "happy-english.log"

    @property
    def docs_enabled(self) -> bool:
        if self.api_docs_enabled is not None:
            return self.api_docs_enabled
        return self.app_env != "production"

    @model_validator(mode="after")
    def production_security(self):
        if self.app_env == "production":
            if not self.cookie_secure or self.secret_key.startswith("replace-"):
                raise ValueError("Production requires COOKIE_SECURE=true and a random SECRET_KEY.")
            if not self.cors_origins or any(
                origin == "*" or not origin.startswith("https://") for origin in self.cors_origins
            ):
                raise ValueError("Production CORS origins must be an explicit HTTPS allowlist.")
            if not self.trusted_hosts or "*" in self.trusted_hosts:
                raise ValueError("Production requires an explicit TRUSTED_HOSTS allowlist.")
            if self.docs_enabled:
                raise ValueError("Production API documentation must be disabled.")
        return self
