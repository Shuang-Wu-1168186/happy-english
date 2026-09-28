import hmac
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError

from app.api import accounts, audio, content, learning_catalog, learning_progress, membership, progress
from app.core.config import Settings
from app.core.database import make_engine
from app.core.security import SESSION_HEADER, read_session
from app.services.wechat import WeChatMiniProgramClient


def create_app(settings: Settings | None = None, engine=None):
    settings = settings or Settings()
    engine = engine if engine is not None else make_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app):
        yield
        close_wechat = getattr(app.state.wechat_miniprogram, "close", None)
        if close_wechat:
            close_wechat()
        engine.dispose()

    app = FastAPI(title="Happy English API", version="1.0.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.engine = engine
    app.state.wechat_miniprogram = WeChatMiniProgramClient(settings)

    @app.middleware("http")
    async def session_and_csrf(request: Request, call_next):
        request.state.session = read_session(request)
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            expected = request.state.session.get("csrf", "")
            supplied = request.headers.get("X-CSRF-Token", "")
            if not expected or not hmac.compare_digest(expected, supplied):
                return JSONResponse(
                    {"detail": "Session expired. Refresh the page and try again."}, status_code=403
                )
        response = await call_next(request)
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "X-CSRF-Token", SESSION_HEADER],
        expose_headers=[SESSION_HEADER],
    )

    @app.exception_handler(IntegrityError)
    async def conflict(request, exc):
        return JSONResponse(
            {"detail": "A record already exists or a related record is missing."}, status_code=409
        )

    async def database_error(request, exc):
        logging.getLogger(__name__).error("Database unavailable: %s", type(exc).__name__)
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
