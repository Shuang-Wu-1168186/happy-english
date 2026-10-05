import sys
from pathlib import Path
from threading import Lock
from types import ModuleType

from tests.conftest import sign_in


def test_request_and_tts_logs_include_timing_without_text(client, monkeypatch, tmp_path):
    cache_file = tmp_path / "fake-tts.wav"
    fake_kokoro = ModuleType("app.audio.kokoro")
    fake_kokoro.KOKORO_VOICE_OPTIONS = {"b": {"default": "test-voice"}}
    fake_kokoro.kokoro_generation_lock = Lock()
    fake_kokoro.get_cache_path = lambda *_args: str(cache_file)
    fake_kokoro.is_valid_audio_file = lambda path: Path(path).is_file()

    def generate(_text, path, *_args):
        Path(path).write_bytes(b"RIFF" + b"\\x00" * 48)

    fake_kokoro.generate_kokoro_audio = generate
    monkeypatch.setitem(sys.modules, "app.audio.kokoro", fake_kokoro)
    client.app.state.settings.audio_enabled = True

    health = client.get("/api/health", headers={"X-Request-ID": "health-log-1"})
    assert health.status_code == 200
    assert health.headers["X-Request-ID"] == "health-log-1"

    preflight = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Request-ID",
        },
    )
    assert preflight.status_code == 200
    assert "x-request-id" in preflight.headers["access-control-allow-headers"].lower()

    response = client.post(
        "/api/audio/tts",
        json={"text": "Private speech content", "lang": "b", "cache": True},
        headers={
            **sign_in(client),
            "Origin": "http://localhost:5173",
            "X-Request-ID": "tts-log-1",
        },
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert "X-Request-ID" in response.headers["access-control-expose-headers"]

    log_contents = (tmp_path / "logs" / "happy-english.log").read_text(encoding="utf-8")
    assert "request_id=health-log-1 http.request.completed" in log_contents
    assert "request_id=tts-log-1 audio.tts.started" in log_contents
    assert "request_id=tts-log-1 audio.tts.cache.miss" in log_contents
    assert "request_id=tts-log-1 audio.tts.completed" in log_contents
    assert "duration_ms=" in log_contents
    assert "Private speech content" not in log_contents
