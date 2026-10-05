"""Kokoro TTS configuration, synthesis, caching, and text preparation."""

import gc
import hashlib
import logging
import os
import re
from threading import Lock
from time import perf_counter

import numpy as np
import soundfile as sf

from app.audio.audio_config import CACHE_DIR


logger = logging.getLogger(__name__)

# This checkpoint supports Mandarin and the compatible English voice below.
KOKORO_REPO_ID = "hexgrad/Kokoro-82M-v1.1-zh"
KOKORO_LANGUAGE = "b"
KOKORO_VOICE = "bf_vale"
KOKORO_CHINESE_LANGUAGE = "z"
KOKORO_CHINESE_VOICE = "zf_001"
KOKORO_VOICE_OPTIONS = {
    KOKORO_LANGUAGE: {
        "default": KOKORO_VOICE,
        "allowed": {KOKORO_VOICE},
    },
    KOKORO_CHINESE_LANGUAGE: {
        "default": KOKORO_CHINESE_VOICE,
        "allowed": {KOKORO_CHINESE_VOICE},
    },
}
KOKORO_SPEED = 1.0
KOKORO_SAMPLE_RATE = 24000
KOKORO_MAX_TEXT_LENGTH = 1000

# Decorative symbols remain visible in cards but are not sent to TTS.
KOKORO_DECORATION_RE = re.compile(
    r"[\U0001F000-\U0001FAFF\u2600-\u27FF\u2E3A\u2E3B\uFE0E\uFE0F\u200D\u20E3]+"
)

os.makedirs(CACHE_DIR, exist_ok=True)

# Importing Kokoro imports PyTorch, so all pipelines are constructed only on
# the first TTS request.
kokoro_pipelines = {}
kokoro_pipeline_lock = Lock()
kokoro_english_g2p_pipeline = None
kokoro_english_g2p_lock = Lock()
kokoro_generation_lock = Lock()


def get_kokoro_english_g2p_pipeline():
    """Return an English phonemizer for English terms in Chinese text."""
    global kokoro_english_g2p_pipeline

    from kokoro import KPipeline

    if kokoro_english_g2p_pipeline is not None:
        return kokoro_english_g2p_pipeline

    with kokoro_english_g2p_lock:
        if kokoro_english_g2p_pipeline is None:
            logger.info("audio.tts.g2p_pipeline.initializing language=%s", KOKORO_LANGUAGE)
            started_at = perf_counter()
            kokoro_english_g2p_pipeline = KPipeline(
                lang_code=KOKORO_LANGUAGE,
                repo_id=KOKORO_REPO_ID,
                model=False,
            )
            logger.info(
                "audio.tts.g2p_pipeline.initialized language=%s duration_ms=%.1f",
                KOKORO_LANGUAGE,
                (perf_counter() - started_at) * 1000,
            )

    return kokoro_english_g2p_pipeline


def phonemise_english_inside_chinese(text: str) -> str:
    """Convert an embedded English segment to Kokoro-compatible phonemes."""
    started_at = perf_counter()
    logger.debug("audio.tts.phonemise.started text_chars=%d", len(text))
    for result in get_kokoro_english_g2p_pipeline()(text):
        phonemes = result.phonemes
        logger.debug(
            "audio.tts.phonemise.completed input_chars=%d output_chars=%d duration_ms=%.1f",
            len(text),
            len(phonemes),
            (perf_counter() - started_at) * 1000,
        )
        return phonemes
    logger.warning("audio.tts.phonemise.empty input_chars=%d", len(text))
    return ""


def get_kokoro_pipeline(language: str = KOKORO_LANGUAGE):
    """Lazily initialise and reuse the pipeline for one supported language."""
    if language not in KOKORO_VOICE_OPTIONS:
        raise ValueError(f"Unsupported Kokoro language: {language}")

    from kokoro import KPipeline

    if language in kokoro_pipelines:
        return kokoro_pipelines[language]

    with kokoro_pipeline_lock:
        if language in kokoro_pipelines:
            return kokoro_pipelines[language]

        logger.info("audio.tts.pipeline.initializing language=%s", language)
        started_at = perf_counter()
        if language == KOKORO_CHINESE_LANGUAGE:
            english_pipeline = kokoro_pipelines.get(KOKORO_LANGUAGE)
            if english_pipeline is None:
                english_pipeline = KPipeline(
                    lang_code=KOKORO_LANGUAGE,
                    repo_id=KOKORO_REPO_ID,
                )
                kokoro_pipelines[KOKORO_LANGUAGE] = english_pipeline

            pipeline_kwargs = {
                "lang_code": language,
                "repo_id": KOKORO_REPO_ID,
                "model": english_pipeline.model,
                "en_callable": phonemise_english_inside_chinese,
            }
        else:
            pipeline_kwargs = {
                "lang_code": language,
                "repo_id": KOKORO_REPO_ID,
            }

        kokoro_pipelines[language] = KPipeline(**pipeline_kwargs)
        logger.info(
            "audio.tts.pipeline.initialized language=%s duration_ms=%.1f",
            language,
            (perf_counter() - started_at) * 1000,
        )

    return kokoro_pipelines[language]


def get_cache_path(
    text: str,
    language: str = KOKORO_LANGUAGE,
    voice: str = KOKORO_VOICE,
    speed: float = KOKORO_SPEED,
) -> str:
    """Return a cache filename unique to the source text and voice settings."""
    cache_key = f"kokoro|{language}|{voice}|{speed}|{text}"
    text_hash = hashlib.md5(cache_key.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{text_hash}.wav")


def is_valid_audio_file(path: str) -> bool:
    """Return whether a generated WAV exists and contains audio data."""
    try:
        return os.path.isfile(path) and os.path.getsize(path) > 44
    except OSError:
        return False


def clean_kokoro_tts_text(text: str) -> str:
    """Remove decorative emoji and normalise whitespace before synthesis."""
    text = KOKORO_DECORATION_RE.sub("", text or "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\r?\n *", "\n", text)
    return text.strip()


def generate_kokoro_audio(
    text: str,
    output_file: str,
    language: str = KOKORO_LANGUAGE,
    voice: str = KOKORO_VOICE,
    speed: float = KOKORO_SPEED,
):
    """Generate a Kokoro WAV file."""
    started_at = perf_counter()
    audio_chunks = []
    audio = None
    audio_data = None
    try:
        text = clean_kokoro_tts_text(text)
        if not text:
            raise ValueError("No speakable text remains after removing decorative symbols.")

        logger.info(
            "audio.tts.synthesis.started language=%s voice=%s speed=%.2f text_chars=%d",
            language,
            voice,
            speed,
            len(text),
        )
        pipeline = get_kokoro_pipeline(language)
        for _, _, audio in pipeline(text, voice=voice, speed=speed):
            if audio is not None:
                audio_chunks.append(np.asarray(audio))

        if not audio_chunks:
            raise RuntimeError("Kokoro generated no audio.")

        audio_data = audio_chunks[0] if len(audio_chunks) == 1 else np.concatenate(audio_chunks)
        sf.write(output_file, audio_data, KOKORO_SAMPLE_RATE)
        output_bytes = os.path.getsize(output_file)
        sample_count = len(audio_data)
        logger.info(
            "audio.tts.synthesis.completed language=%s voice=%s chunks=%d samples=%d audio_ms=%.1f output_bytes=%d duration_ms=%.1f",
            language,
            voice,
            len(audio_chunks),
            sample_count,
            sample_count / KOKORO_SAMPLE_RATE * 1000,
            output_bytes,
            (perf_counter() - started_at) * 1000,
        )

    except (RuntimeError, OSError, ValueError) as exc:
        logger.error(
            "audio.tts.synthesis.failed language=%s voice=%s error_type=%s duration_ms=%.1f",
            language,
            voice,
            type(exc).__name__,
            (perf_counter() - started_at) * 1000,
        )
        raise

    finally:
        # Release request-local arrays whether inference succeeds or fails.
        audio_chunks.clear()
        del audio, audio_data
        gc.collect()


def build_note_card_tts_payload(item: dict) -> dict | None:
    """Build one complete TTS payload from a database note-card row."""
    english_text = item.get("english_text") or item.get("item_title") or item.get("raw_text") or ""
    fields = [
        english_text,
        item.get("chinese_text"),
        item.get("explanation"),
        item.get("examples"),
        item.get("example_image_alt"),
    ]
    text = "\n\n".join(
        clean_text
        for field in fields
        if (clean_text := clean_kokoro_tts_text(field)) and clean_text != "No extra notes yet."
    )
    if not text:
        return None

    language = KOKORO_CHINESE_LANGUAGE if re.search(r"[\u3400-\u9fff]", text) else KOKORO_LANGUAGE
    voice = KOKORO_CHINESE_VOICE if language == KOKORO_CHINESE_LANGUAGE else KOKORO_VOICE
    return {"text": text, "language": language, "voice": voice}
