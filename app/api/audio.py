import logging
import os
import tempfile
from pathlib import Path
from threading import Lock

from fastapi import APIRouter, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.api.dependencies import User
from app.audio.assessment import calculate_assessment_score
from app.schemas import TTSInput

router = APIRouter(prefix="/audio", tags=["audio"])
whisper_model = None
whisper_lock = Lock()


def require_audio(request):
    if not request.app.state.settings.audio_enabled:
        raise HTTPException(
            503, "Server audio is disabled. Install requirements-audio.txt and set AUDIO_ENABLED=true."
        )


@router.post("/tts")
def tts(data: TTSInput, request: Request, user: User):
    require_audio(request)
    try:
        from app.audio.kokoro import (
            KOKORO_VOICE_OPTIONS,
            generate_kokoro_audio,
            get_cache_path,
            is_valid_audio_file,
            kokoro_generation_lock,
        )

        voice = KOKORO_VOICE_OPTIONS[data.lang]["default"]
        path = get_cache_path(data.text, data.lang, voice, data.speed)
        with kokoro_generation_lock:
            if not data.cache or not is_valid_audio_file(path):
                generate_kokoro_audio(data.text, path, data.lang, voice, data.speed)
        return FileResponse(path, media_type="audio/wav")
    except (ImportError, RuntimeError, OSError, ValueError) as exc:
        logging.getLogger(__name__).exception("TTS failed")
        raise HTTPException(
            503, "Speech model unavailable. Check audio dependencies and model configuration."
        ) from exc


@router.post("/assessment")
def assessment(
    request: Request,
    user: User,
    audio: UploadFile,
    reference_text: str = Form(..., min_length=1, max_length=500),
):
    require_audio(request)
    data = audio.file.read(10 * 1024 * 1024 + 1)
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(413, "Audio must be smaller than 10 MB.")
    if not data:
        raise HTTPException(400, "Audio is empty.")
    path = None
    try:
        global whisper_model
        with tempfile.NamedTemporaryFile(suffix=".audio", delete=False) as file:
            file.write(data)
            path = file.name
        with whisper_lock:
            if whisper_model is None:
                from faster_whisper import WhisperModel

                whisper_model = WhisperModel(
                    os.getenv("WHISPER_MODEL", "base.en"),
                    device=os.getenv("WHISPER_DEVICE", "cpu"),
                    compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
                )
            segments, _ = whisper_model.transcribe(
                path, language="en", beam_size=5, vad_filter=True, condition_on_previous_text=False
            )
            transcript = " ".join(segment.text.strip() for segment in segments).strip()
        return {
            "score": calculate_assessment_score(reference_text, transcript),
            "transcript": transcript,
            "reference_text": reference_text,
            "score_type": "transcription_match",
        }
    except (ImportError, RuntimeError, OSError, ValueError) as exc:
        logging.getLogger(__name__).exception("Assessment failed")
        raise HTTPException(
            503, "Audio could not be assessed. Check the recording and server model configuration."
        ) from exc
    finally:
        if path:
            Path(path).unlink(missing_ok=True)
