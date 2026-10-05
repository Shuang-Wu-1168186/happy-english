import logging
import os
import tempfile
from pathlib import Path
from threading import Lock
from time import perf_counter

from fastapi import APIRouter, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from app.api.dependencies import User
from app.audio.assessment import calculate_assessment_score
from app.schemas import TTSInput

router = APIRouter(prefix="/audio", tags=["audio"])
whisper_model = None
whisper_lock = Lock()
logger = logging.getLogger(__name__)
MAX_AUDIO_BYTES = 10 * 1024 * 1024


def require_audio(request):
    if not request.app.state.settings.audio_enabled:
        logger.warning("audio.request.rejected reason=disabled path=%s", request.url.path)
        raise HTTPException(
            503, "Server audio is disabled. Install requirements-audio.txt and set AUDIO_ENABLED=true."
        )


@router.post("/tts")
def tts(data: TTSInput, request: Request, user: User):
    require_audio(request)
    started_at = perf_counter()
    text_length = len(data.text)
    logger.info(
        "audio.tts.started language=%s text_chars=%d speed=%.2f cache_requested=%s",
        data.lang,
        text_length,
        data.speed,
        data.cache,
    )
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
        lock_started_at = perf_counter()
        with kokoro_generation_lock:
            lock_wait_ms = (perf_counter() - lock_started_at) * 1000
            cache_hit = bool(data.cache and is_valid_audio_file(path))
            if cache_hit:
                logger.info(
                    "audio.tts.cache.hit language=%s voice=%s lock_wait_ms=%.1f",
                    data.lang,
                    voice,
                    lock_wait_ms,
                )
            else:
                logger.info(
                    "audio.tts.cache.miss language=%s voice=%s lock_wait_ms=%.1f",
                    data.lang,
                    voice,
                    lock_wait_ms,
                )
                generate_kokoro_audio(data.text, path, data.lang, voice, data.speed)
        audio_bytes = Path(path).stat().st_size
        logger.info(
            "audio.tts.completed language=%s voice=%s cache_hit=%s audio_bytes=%d duration_ms=%.1f",
            data.lang,
            voice,
            cache_hit,
            audio_bytes,
            (perf_counter() - started_at) * 1000,
        )
        return FileResponse(path, media_type="audio/wav")
    except (ImportError, RuntimeError, OSError, ValueError) as exc:
        logger.error(
            "audio.tts.failed language=%s text_chars=%d error_type=%s duration_ms=%.1f",
            data.lang,
            text_length,
            type(exc).__name__,
            (perf_counter() - started_at) * 1000,
        )
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
    started_at = perf_counter()
    path = None
    try:
        read_started_at = perf_counter()
        data = audio.file.read(MAX_AUDIO_BYTES + 1)
        read_duration_ms = (perf_counter() - read_started_at) * 1000
        if len(data) > MAX_AUDIO_BYTES:
            logger.warning(
                "audio.assessment.rejected reason=too_large input_bytes=%d read_duration_ms=%.1f",
                len(data),
                read_duration_ms,
            )
            raise HTTPException(413, "Audio must be smaller than 10 MB.")
        if not data:
            logger.warning("audio.assessment.rejected reason=empty read_duration_ms=%.1f", read_duration_ms)
            raise HTTPException(400, "Audio is empty.")
        logger.info(
            "audio.assessment.started input_bytes=%d read_duration_ms=%.1f",
            len(data),
            read_duration_ms,
        )

        temporary_write_started_at = perf_counter()
        global whisper_model
        with tempfile.NamedTemporaryFile(suffix=".audio", delete=False) as file:
            file.write(data)
            path = file.name
        logger.debug(
            "audio.assessment.temporary_file_written input_bytes=%d duration_ms=%.1f",
            len(data),
            (perf_counter() - temporary_write_started_at) * 1000,
        )

        model_name = os.getenv("WHISPER_MODEL", "base.en")
        device = os.getenv("WHISPER_DEVICE", "cpu")
        compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        lock_started_at = perf_counter()
        with whisper_lock:
            lock_wait_ms = (perf_counter() - lock_started_at) * 1000
            if whisper_model is None:
                from faster_whisper import WhisperModel

                logger.info(
                    "audio.assessment.model.initializing model=%s device=%s compute_type=%s",
                    model_name,
                    device,
                    compute_type,
                )
                model_started_at = perf_counter()
                whisper_model = WhisperModel(model_name, device=device, compute_type=compute_type)
                logger.info(
                    "audio.assessment.model.initialized model=%s duration_ms=%.1f",
                    model_name,
                    (perf_counter() - model_started_at) * 1000,
                )

            logger.info(
                "audio.assessment.transcription.started model=%s lock_wait_ms=%.1f",
                model_name,
                lock_wait_ms,
            )
            transcription_started_at = perf_counter()
            segments, _ = whisper_model.transcribe(
                path, language="en", beam_size=5, vad_filter=True, condition_on_previous_text=False
            )
            transcript_parts = []
            segment_count = 0
            for segment in segments:
                segment_count += 1
                text = segment.text.strip()
                if text:
                    transcript_parts.append(text)
            transcript = " ".join(transcript_parts).strip()
            logger.info(
                "audio.assessment.transcription.completed model=%s segments=%d transcript_chars=%d duration_ms=%.1f",
                model_name,
                segment_count,
                len(transcript),
                (perf_counter() - transcription_started_at) * 1000,
            )

        score_started_at = perf_counter()
        score = calculate_assessment_score(reference_text, transcript)
        logger.info(
            "audio.assessment.completed input_bytes=%d transcript_chars=%d score=%d scoring_ms=%.1f duration_ms=%.1f",
            len(data),
            len(transcript),
            score,
            (perf_counter() - score_started_at) * 1000,
            (perf_counter() - started_at) * 1000,
        )
        return {
            "score": score,
            "transcript": transcript,
            "reference_text": reference_text,
            "score_type": "transcription_match",
        }
    except HTTPException:
        raise
    except (ImportError, RuntimeError, OSError, ValueError) as exc:
        logger.error(
            "audio.assessment.failed error_type=%s duration_ms=%.1f",
            type(exc).__name__,
            (perf_counter() - started_at) * 1000,
        )
        raise HTTPException(
            503, "Audio could not be assessed. Check the recording and server model configuration."
        ) from exc
    finally:
        if path:
            Path(path).unlink(missing_ok=True)
