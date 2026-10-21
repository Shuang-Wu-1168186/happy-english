import logging
import re
from time import perf_counter

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session


logger = logging.getLogger("app.sql")
_SENSITIVE_SQL = re.compile(
    r"(?:password|passwd|secret|token|authorization|cookie|csrf|api[_-]?key|access[_-]?key|signature)",
    re.IGNORECASE,
)
_MAX_PARAMETER_TEXT = 2048


def _log_parameter(value, key=None, statement=""):
    if (key and _SENSITIVE_SQL.search(str(key))) or _SENSITIVE_SQL.search(statement):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): _log_parameter(item_value, item_key, statement) for item_key, item_value in value.items()}
    if isinstance(value, (list, tuple)):
        return [_log_parameter(item, statement=statement) for item in value]
    if isinstance(value, bytes):
        return f"<bytes:{len(value)}>"
    if isinstance(value, str) and len(value) > _MAX_PARAMETER_TEXT:
        return f"{value[:_MAX_PARAMETER_TEXT]}...[truncated]"
    return value


def _format_parameters(parameters, statement):
    if parameters is None:
        return None
    return _log_parameter(parameters, statement=statement)


def configure_sql_logging(engine):
    """Log every SQL statement and its bound conditions for this engine."""
    if getattr(engine, "_happy_sql_logging_configured", False):
        return engine

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(connection, cursor, statement, parameters, context, executemany):
        context._happy_sql_started = perf_counter()
        context._happy_sql_parameters = parameters
        context._happy_sql_statement = statement

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(connection, cursor, statement, parameters, context, executemany):
        started = getattr(context, "_happy_sql_started", None)
        duration_ms = (perf_counter() - started) * 1000 if started else 0
        compiled_parameters = getattr(context, "compiled_parameters", None)
        logger.info(
            "sql.query statement=%s params=%s duration_ms=%.1f rowcount=%s executemany=%s",
            statement,
            _format_parameters(
                compiled_parameters
                if compiled_parameters is not None
                else getattr(context, "_happy_sql_parameters", parameters),
                statement,
            ),
            duration_ms,
            cursor.rowcount,
            executemany,
        )

    @event.listens_for(engine, "handle_error")
    def handle_sql_error(exception_context):
        statement = exception_context.statement or ""
        logger.error(
            "sql.error statement=%s params=%s error_type=%s",
            statement,
            _format_parameters(exception_context.parameters, statement),
            type(exception_context.original_exception).__name__,
        )

    @event.listens_for(engine, "commit")
    def log_commit(connection):
        logger.info("sql.transaction action=commit")

    @event.listens_for(engine, "rollback")
    def log_rollback(connection):
        logger.info("sql.transaction action=rollback")

    engine._happy_sql_logging_configured = True
    return engine


def make_engine(url: str):
    options = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
    else:
        options.update(
            pool_recycle=1800,
            pool_size=10,
            max_overflow=10,
            connect_args={"connect_timeout": 5, "read_timeout": 30, "write_timeout": 30},
        )
    return configure_sql_logging(create_engine(url, **options))


def session_scope(engine):
    """One unit of work per request; services commit before returning a success."""
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
