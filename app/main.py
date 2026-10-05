import hmac
import logging
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

from app.api import accounts, audio, content, learning_catalog, learning_progress, membership, progress
from app.core.config import Settings
from app.core.database import make_engine
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


def create_app(settings: Settings | None = None, engine=None):
    settings = settings or Settings()
    configure_logging(settings)
    engine = engine if engine is not None else make_engine(settings.database_url)

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

    app = FastAPI(title="Happy English API", version="1.0.0", lifespan=lifespan)
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
        is_api_request = request.url.path.startswith("/api/")
        try:
            request.state.session = read_session(request)
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
            if is_api_request:
                response.headers["Cache-Control"] = "no-store"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        except Exception as exc:
            logger.error(
                "http.request.failed method=%s path=%s error_type=%s duration_ms=%.1f",
                request.method,
                request.url.path,
                type(exc).__name__,
                (perf_counter() - started_at) * 1000,
            )
            raise
        finally:
            if response is not None and is_api_request:
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
                    "%s method=%s path=%s status=%d duration_ms=%.1f",
                    message,
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
    app.include_router(content.router, prefix="/api")
    app.include_router(learning_catalog.router, prefix="/api")
    app.include_router(membership.router, prefix="/api")
    app.include_router(learning_progress.router, prefix="/api")
    app.include_router(progress.router, prefix="/api")
    app.include_router(audio.router, prefix="/api")
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    return app
