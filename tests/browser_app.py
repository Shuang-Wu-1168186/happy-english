"""Isolated, disposable database for UI integration tests. Never uses .env or the user's database."""

import tempfile
from pathlib import Path
from app.core.config import Settings
from app.main import create_app
from tests.support import sample_engine

root = Path(tempfile.mkdtemp(prefix="happy-english-e2e-"))
app = create_app(
    Settings(
        _env_file=None,
        secret_key="browser-test-secret-key-123456789012",
        static_dir=root / "static",
        uploads_dir=root / "static" / "uploads",
        log_dir=root / "logs",
        log_console=False,
        audio_enabled=False,
    ),
    sample_engine(f"sqlite:///{root / 'browser.sqlite3'}"),
)
