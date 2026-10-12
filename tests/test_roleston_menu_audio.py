import sys
from pathlib import Path
from threading import Lock
from types import ModuleType

from app.services.roleston_menu import ROLLESTON_MENU_TTS_TEXTS


def test_public_menu_tts_uses_the_project_kokoro_service(client, monkeypatch, tmp_path):
    cache_file = tmp_path / "menu-tts.wav"
    generated_texts = []
    cache_requests = []
    fake_kokoro = ModuleType("app.audio.kokoro")
    fake_kokoro.KOKORO_VOICE_OPTIONS = {"b": {"default": "test-voice"}}
    fake_kokoro.kokoro_generation_lock = Lock()

    def get_cache_path(text, language, voice, speed):
        cache_requests.append((text, language, voice, speed))
        return str(cache_file)

    def generate(text, path, *_args):
        generated_texts.append(text)
        Path(path).write_bytes(b"RIFF" + b"\x00" * 48)

    fake_kokoro.get_cache_path = get_cache_path
    fake_kokoro.is_valid_audio_file = lambda path: Path(path).is_file()
    fake_kokoro.generate_kokoro_audio = generate
    monkeypatch.setitem(sys.modules, "app.audio.kokoro", fake_kokoro)
    client.app.state.settings.audio_enabled = True

    response = client.get("/api/audio/menu-tts/fish-and-chips-1")

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content.startswith(b"RIFF")
    assert generated_texts == ["Battered fish. 4 dollars and 90 cents."]
    assert cache_requests == [
        (ROLLESTON_MENU_TTS_TEXTS["fish-and-chips-1"], "b", "test-voice", 0.82)
    ]


def test_public_menu_tts_rejects_unknown_menu_items(client):
    response = client.get("/api/audio/menu-tts/not-a-menu-item")

    assert response.status_code == 404
    assert response.json() == {"detail": "Menu audio item not found."}
