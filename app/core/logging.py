"""Application logging with rotating files and request correlation IDs."""

import logging
import re
from contextvars import ContextVar, Token
from logging.handlers import RotatingFileHandler
from pathlib import Path
from uuid import uuid4


APP_LOGGER_NAME = "app"
REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID = ContextVar("happy_english_request_id", default="-")
_REQUEST_ID_RE = re.compile(r"[A-Za-z0-9._-]{1,64}")
_MANAGED_HANDLER_MARKER = "_happy_english_managed_handler"
_FORMAT = "%(asctime)s %(levelname)s [%(name)s] request_id=%(request_id)s %(message)s"


class RequestContextFilter(logging.Filter):
    """Add the current request ID to every application log record."""

    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = _REQUEST_ID.get()
        return True


def new_request_id(candidate: str | None = None) -> str:
    """Keep a valid upstream ID or generate a short safe correlation ID."""
    if candidate and _REQUEST_ID_RE.fullmatch(candidate):
        return candidate
    return uuid4().hex


def bind_request_id(request_id: str) -> Token:
    return _REQUEST_ID.set(request_id)


def reset_request_id(token: Token) -> None:
    _REQUEST_ID.reset(token)


def _handler(formatter, level):
    context_filter = RequestContextFilter()

    def configure(handler):
        handler.setLevel(level)
        handler.setFormatter(formatter)
        handler.addFilter(context_filter)
        setattr(handler, _MANAGED_HANDLER_MARKER, True)
        return handler

    return configure


def _remove_managed_handlers(logger) -> None:
    for handler in tuple(logger.handlers):
        if getattr(handler, _MANAGED_HANDLER_MARKER, False):
            logger.removeHandler(handler)
            handler.close()


def configure_logging(settings) -> logging.Logger:
    """Configure the application logger once per app factory invocation.

    The file handler rotates before it grows without bound.  Only handlers
    created by this function are replaced, so host-provided logging handlers
    remain untouched.
    """
    log_dir = Path(settings.log_dir).expanduser()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "happy-english.log"

    logger = logging.getLogger(APP_LOGGER_NAME)
    level = getattr(logging, settings.log_level)
    logger.setLevel(level)
    logger.propagate = False
    _remove_managed_handlers(logger)

    formatter = logging.Formatter(_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
    configure_handler = _handler(formatter, level)
    logger.addHandler(
        configure_handler(
            RotatingFileHandler(
                log_file,
                maxBytes=settings.log_max_bytes,
                backupCount=settings.log_backup_count,
                encoding="utf-8",
            )
        )
    )
    if settings.log_console:
        logger.addHandler(configure_handler(logging.StreamHandler()))

    logger.info(
        "logging.configured file=%s level=%s max_bytes=%d backup_count=%d",
        log_file,
        settings.log_level,
        settings.log_max_bytes,
        settings.log_backup_count,
    )
    return logger
