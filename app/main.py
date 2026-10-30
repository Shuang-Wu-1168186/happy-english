import hmac
import json
import logging
import re
from contextlib import asynccontextmanager
from ipaddress import ip_address
from time import perf_counter
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api import (
    accounts,
    analytics,
    audio,
    app_shell,
    content,
    learning_catalog,
    learning_progress,
    membership,
    private_zone,
    progress,
    request_audit,
    vocabulary,
)
from app.core.config import Settings
from app.core.database import configure_sql_logging, make_engine
from app.core.logging import (
    REQUEST_ID_HEADER,
    bind_request_id,
    configure_logging,
    new_request_id,
    reset_request_id,
)
from app.core.security import SESSION_HEADER, read_session
from app.services.wechat import WeChatMiniProgramClient


logger = logging.getLogger(__name__)

_REQUEST_LOG_MAX_BYTES = 64 * 1024
_REQUEST_LOG_MAX_TEXT = 4096
_SENSITIVE_LOG_KEY = re.compile(
    r"(?:password|passwd|secret|token|authorization|cookie|csrf|api[_-]?key|access[_-]?key|signature)",
    re.IGNORECASE,
)


def _redact_log_value(value, key=None):
    """Make request/response logging useful without copying credentials to logs."""
    if key and _SENSITIVE_LOG_KEY.search(str(key)):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): _redact_log_value(item_value, item_key) for item_key, item_value in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redact_log_value(item) for item in value]
    if isinstance(value, str) and len(value) > _REQUEST_LOG_MAX_TEXT:
        return f"{value[:_REQUEST_LOG_MAX_TEXT]}...[truncated]"
    return value


def _json_for_log(value):
    try:
        return json.dumps(_redact_log_value(value), ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError):
        return json.dumps({"value": str(value)}, ensure_ascii=False)


def _request_actor_for_log(request: Request):
    """Return a small identity context without copying session credentials."""
    user = getattr(request.state, "user", None)
    if user:
        return user.get("id"), user.get("username") or "-"
    session = getattr(request.state, "session", {})
    return session.get("uid") or "-", "-"


def _request_ip_for_log(request: Request):
    """Return the client address supplied by the trusted proxy or socket."""
    candidates = [request.headers.get("X-Real-IP", "")]
    if request.client:
        candidates.append(request.client.host)
    for candidate in candidates:
        try:
            return str(ip_address(candidate.strip()))
        except ValueError:
            continue
    return "-"


async def _request_input_for_log(request: Request):
    """Capture structured request input while skipping binary upload bodies."""
    content_type = request.headers.get("content-type", "").split(";", 1)[0].lower()
    result = {
        "path_params": dict(request.path_params),
        "query": {key: values for key, values in parse_qs(request.url.query, keep_blank_values=True).items()},
    }
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return result
    content_length = int(request.headers.get("content-length", "0") or 0)
    if content_type.startswith("multipart/"):
        result["body"] = {
            "omitted": "multipart body",
            "content_type": content_type,
            "content_length": content_length,
        }
        return result
    if content_length > _REQUEST_LOG_MAX_BYTES:
        result["body"] = {
            "omitted": "request body too large",
            "content_type": content_type,
            "content_length": content_length,
        }
        return result
    body = await request.body()
    if not body:
        result["body"] = None
        return result
    if len(body) > _REQUEST_LOG_MAX_BYTES:
        result["body"] = {
            "omitted": "request body too large",
            "content_type": content_type,
            "content_length": len(body),
        }
        return result
    if content_type == "application/json" or content_type.endswith("+json"):
        try:
            result["body"] = json.loads(body.decode("utf-8"))
            # Speech requests can contain private learner text. Keep the
            # request shape in diagnostics without copying that text to logs.
            if request.url.path == "/api/audio/tts" and isinstance(result["body"], dict):
                result["body"] = {**result["body"], "text": "[REDACTED]"}
            # Analytics accepts only validated scalar properties, but logging
            # its raw payload would still create an unnecessary second copy of
            # learner behaviour data (including stable resource references).
            if request.url.path.startswith("/api/analytics/"):
                events = result["body"].get("events", []) if isinstance(result["body"], dict) else []
                result["body"] = {
                    "omitted": "analytics payload",
                    "event_count": len(events) if isinstance(events, list) else 0,
                }
        except (UnicodeDecodeError, json.JSONDecodeError):
            result["body"] = {"omitted": "invalid JSON body", "bytes": len(body)}
    elif content_type == "application/x-www-form-urlencoded":
        result["body"] = {key: values for key, values in parse_qs(body.decode("utf-8"), keep_blank_values=True).items()}
    elif content_type.startswith("text/"):
        result["body"] = body.decode("utf-8", errors="replace")
    else:
        result["body"] = {"omitted": "binary body", "content_type": content_type, "bytes": len(body)}
    return result


def _response_output_for_log(response):
    """Capture JSON/text responses; describe streamed files without reading them."""
    content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
    body = getattr(response, "body", None)
    if body is None:
        return {"omitted": "streaming response", "content_type": content_type}
    if content_type == "application/json" or content_type.endswith("+json"):
        try:
            return json.loads(body[:_REQUEST_LOG_MAX_BYTES].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {"omitted": "response body too large or invalid JSON", "bytes": len(body)}
    if content_type.startswith("text/"):
        return body[:_REQUEST_LOG_MAX_BYTES].decode("utf-8", errors="replace")
    return {"omitted": "binary response", "content_type": content_type, "bytes": len(body)}


async def _materialise_text_response_for_log(response):
    """Read JSON/text streaming responses once, then return an equivalent response."""
    content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
    if getattr(response, "body", None) is not None or not (
        content_type == "application/json"
        or content_type.endswith("+json")
        or content_type.startswith("text/")
    ):
        return response
    body_iterator = getattr(response, "body_iterator", None)
    if body_iterator is None:
        return response
    chunks = []
    async for chunk in body_iterator:
        chunks.append(chunk.encode("utf-8") if isinstance(chunk, str) else chunk)
    body = b"".join(chunks)
    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        background=getattr(response, "background", None),
    )


def create_app(settings: Settings | None = None, engine=None):
    settings = settings or Settings()
    configure_logging(settings)
    engine = engine if engine is not None else make_engine(settings.database_url)
    configure_sql_logging(engine)

    @asynccontextmanager
    async def lifespan(app):
        logger.info("app.lifespan.started environment=%s", settings.app_env)
        try:
            yield
        finally:
            close_wechat = getattr(app.state.wechat_miniprogram, "close", None)
            if close_wechat:
                close_wechat()
            engine.dispose()
            logger.info("app.lifespan.stopped")

    app = FastAPI(
        title="Happy English API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )
    app.state.settings = settings
    app.state.engine = engine
    app.state.wechat_miniprogram = WeChatMiniProgramClient(settings)

    @app.middleware("http")
    async def session_and_csrf(request: Request, call_next):
        request_id = new_request_id(request.headers.get(REQUEST_ID_HEADER))
        request.state.request_id = request_id
        context_token = bind_request_id(request_id)
        started_at = perf_counter()
        response = None
        response_output = None
        is_api_request = request.url.path.startswith("/api/")
        try:
            request.state.session = read_session(request)
            request_input = await _request_input_for_log(request)
            actor_user_id, actor_username = _request_actor_for_log(request)
            request_ip = _request_ip_for_log(request)
            logger.info(
                "http.request.input actor_user_id=%s actor_username=%s ip=%s method=%s path=%s data=%s",
                actor_user_id,
                actor_username,
                request_ip,
                request.method,
                request.url.path,
                _json_for_log(request_input),
            )
            if request.method not in {"GET", "HEAD", "OPTIONS"}:
                expected = request.state.session.get("csrf", "")
                supplied = request.headers.get("X-CSRF-Token", "")
                if not expected or not hmac.compare_digest(expected, supplied):
                    response = JSONResponse(
                        {"detail": "Session expired. Refresh the page and try again."}, status_code=403
                    )
                else:
                    response = await call_next(request)
            else:
                response = await call_next(request)
            response = await _materialise_text_response_for_log(response)
            response_output = _response_output_for_log(response)
            if is_api_request:
                response.headers["Cache-Control"] = "no-store"
            response.headers.setdefault("X-Content-Type-Options", "nosniff")
            response.headers.setdefault("X-Frame-Options", "DENY")
            response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
            response.headers.setdefault(
                "Permissions-Policy", "camera=(), geolocation=(), microphone=(self), payment=()"
            )
            response.headers.setdefault(
                "Content-Security-Policy",
                "base-uri 'self'; frame-ancestors 'none'; object-src 'none'; form-action 'self'",
            )
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        except Exception as exc:
            actor_user_id, actor_username = _request_actor_for_log(request)
            request_ip = _request_ip_for_log(request)
            logger.error(
                "http.request.failed actor_user_id=%s actor_username=%s ip=%s method=%s path=%s error_type=%s duration_ms=%.1f",
                actor_user_id,
                actor_username,
                request_ip,
                request.method,
                request.url.path,
                type(exc).__name__,
                (perf_counter() - started_at) * 1000,
            )
            raise
        finally:
            if response is not None:
                actor_user_id, actor_username = _request_actor_for_log(request)
                duration_ms = (perf_counter() - started_at) * 1000
                logger.info(
                    "http.request.output actor_user_id=%s actor_username=%s method=%s path=%s status=%d data=%s",
                    actor_user_id,
                    actor_username,
                    request.method,
                    request.url.path,
                    response.status_code,
                    _json_for_log(response_output if response_output is not None else _response_output_for_log(response)),
                )
            if response is not None and is_api_request:
                actor_user_id, actor_username = _request_actor_for_log(request)
                request_ip = _request_ip_for_log(request)
                duration_ms = (perf_counter() - started_at) * 1000
                message = "http.request.completed"
                log_method = logger.info
                if settings.request_slow_ms and duration_ms >= settings.request_slow_ms:
                    message = "http.request.slow"
                    log_method = logger.warning
                elif response.status_code >= 500:
                    log_method = logger.error
                elif response.status_code >= 400:
                    log_method = logger.warning
                log_method(
                    "%s actor_user_id=%s actor_username=%s ip=%s method=%s path=%s status=%d duration_ms=%.1f",
                    message,
                    actor_user_id,
                    actor_username,
                    request_ip,
                    request.method,
                    request.url.path,
                    response.status_code,
                    duration_ms,
                )
            reset_request_id(context_token)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "X-CSRF-Token", SESSION_HEADER, REQUEST_ID_HEADER],
        expose_headers=[SESSION_HEADER, REQUEST_ID_HEADER],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)

    @app.exception_handler(IntegrityError)
    async def conflict(request, exc):
        return JSONResponse(
            {"detail": "A record already exists or a related record is missing."}, status_code=409
        )

    async def database_error(request, exc):
        logger.error("database.unavailable path=%s error_type=%s", request.url.path, type(exc).__name__)
        return JSONResponse(
            {"detail": "Database unavailable or schema missing. Check the backend database configuration."},
            status_code=503,
        )

    app.add_exception_handler(OperationalError, database_error)
    app.add_exception_handler(ProgrammingError, database_error)

    @app.get("/api/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "happy-english"}

    @app.get("/api/health/ready", tags=["health"])
    def ready():
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}

    app.include_router(accounts.router, prefix="/api")
    app.include_router(analytics.router, prefix="/api")
    app.include_router(analytics.admin_router, prefix="/api")
    app.include_router(app_shell.router, prefix="/api")
    app.include_router(content.router, prefix="/api")
    app.include_router(learning_catalog.router, prefix="/api")
    app.include_router(membership.router, prefix="/api")
    app.include_router(private_zone.router, prefix="/api")
    app.include_router(learning_progress.router, prefix="/api")
    app.include_router(progress.router, prefix="/api")
    app.include_router(request_audit.router, prefix="/api")
    app.include_router(vocabulary.router, prefix="/api")
    app.include_router(audio.router, prefix="/api")
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    return app
