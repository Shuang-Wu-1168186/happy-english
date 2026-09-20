from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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
    return create_engine(url, **options)


def session_scope(engine):
    """One unit of work per request; services commit before returning a success."""
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
