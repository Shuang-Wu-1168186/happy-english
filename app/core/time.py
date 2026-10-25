"""Small helpers for the UTC-naive timestamps used by MySQL DATETIME fields."""

from datetime import UTC, datetime


def utc_now_naive() -> datetime:
    """Return the current UTC instant without a timezone marker for DATETIME."""

    return datetime.now(UTC).replace(tzinfo=None)
