"""Read structured HTTP request records from the rotating application logs."""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import date, datetime
from math import floor
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import HTTPException


_REQUEST_LOG_RE = re.compile(
    r"^(?P<logged_at>\S+)\s+\S+\s+\[[^]]+\]\s+"
    r"request_id=(?P<request_id>\S+)\s+"
    r"http\.request\.(?P<event>completed|slow|failed)\s+"
    r"actor_user_id=(?P<user_id>\S+)\s+"
    r"actor_username=(?P<username>\S+)\s+"
    r"(?:ip=(?P<ip>\S+)\s+)?"
    r"method=(?P<method>\S+)\s+"
    r"path=(?P<path>\S+)"
    r"(?:\s+status=(?P<status>\d+))?"
    r"(?:\s+error_type=\S+)?"
    r"(?:\s+duration_ms=(?P<duration_ms>[0-9.]+))?"
)
_REPORT_TIMEZONE = ZoneInfo("Pacific/Auckland")


def _parse_timestamp(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z").astimezone(_REPORT_TIMEZONE)
    except ValueError:
        return None


def _log_paths(settings):
    base = Path(settings.log_file)
    paths = [base] if base.is_file() else []
    paths.extend(sorted(base.parent.glob(f"{base.name}.*")))
    return paths


def _percentile(values, percentage):
    """Return an interpolated percentile in milliseconds."""
    ordered = sorted(value for value in values if value is not None)
    if not ordered:
        return None
    position = (len(ordered) - 1) * percentage / 100
    lower = floor(position)
    upper = min(lower + 1, len(ordered) - 1)
    value = ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return round(value, 1)


def _duration_stats(records):
    durations = [record["duration_ms"] for record in records if record["duration_ms"] is not None]
    return {
        "avg_duration_ms": round(sum(durations) / len(durations), 1) if durations else None,
        "p50_ms": _percentile(durations, 50),
        "p90_ms": _percentile(durations, 90),
        "p95_ms": _percentile(durations, 95),
        "p99_ms": _percentile(durations, 99),
        "duration_samples": len(durations),
    }


def _is_error(record):
    return record["event"] == "failed" or (record["status"] is not None and record["status"] >= 400)


def _endpoint_pattern(path):
    """Group numeric and opaque resource IDs under the same API route."""
    return re.sub(r"(?<=/)(?:\d+|hei1_[A-Za-z0-9_-]+)(?=/|$)", ":id", path)


class RequestAuditService:
    """Query API request activity without copying request bodies or secrets."""

    def __init__(self, settings):
        self.settings = settings

    def _records(self):
        records = []
        for path in _log_paths(self.settings):
            try:
                with path.open("r", encoding="utf-8", errors="replace") as stream:
                    for line in stream:
                        match = _REQUEST_LOG_RE.match(line.rstrip("\n"))
                        if not match:
                            continue
                        values = match.groupdict()
                        timestamp = _parse_timestamp(values["logged_at"])
                        if not timestamp or not values["path"].startswith("/api/"):
                            continue
                        records.append(
                            {
                                "logged_at": values["logged_at"],
                                "_timestamp": timestamp,
                                "request_id": values["request_id"],
                                "username": None if values["username"] == "-" else values["username"],
                                "ip": None if not values["ip"] or values["ip"] == "-" else values["ip"],
                                "method": values["method"],
                                "path": values["path"],
                                "status": int(values["status"]) if values["status"] else None,
                                "duration_ms": float(values["duration_ms"])
                                if values["duration_ms"]
                                else None,
                                "event": values["event"],
                            }
                        )
            except OSError:
                continue
        return records

    def _filtered_records(
        self,
        *,
        username="",
        path="",
        method="",
        status=None,
        start_date=None,
        end_date=None,
        include_anonymous=True,
    ):
        if start_date and end_date and start_date > end_date:
            raise HTTPException(422, "Start date must not be after end date.")

        username = username.strip().lower()
        path = path.strip().lower()
        method = method.strip().upper()
        records = []
        for record in self._records():
            if not include_anonymous and record["username"] is None:
                continue
            if username and username not in (record["username"] or "").lower():
                continue
            if path and path not in record["path"].lower():
                continue
            if method and method != record["method"]:
                continue
            if status is not None and status != record["status"]:
                continue
            timestamp = record["_timestamp"]
            if start_date and timestamp.date() < start_date:
                continue
            if end_date and timestamp.date() > end_date:
                continue
            records.append(record)
        return records

    def list(
        self,
        *,
        username: str,
        path: str,
        method: str,
        status: int | None,
        start_date: date | None,
        end_date: date | None,
        page: int,
        page_size: int,
    ):
        records = self._filtered_records(
            username=username,
            path=path,
            method=method,
            status=status,
            start_date=start_date,
            end_date=end_date,
            include_anonymous=False,
        )

        records.sort(key=lambda record: record["_timestamp"], reverse=True)
        total = len(records)
        offset = (page - 1) * page_size
        items = [
            {key: value for key, value in record.items() if key != "_timestamp"}
            for record in records[offset : offset + page_size]
        ]
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    def report(
        self,
        *,
        username="",
        path="",
        method="",
        status=None,
        start_date=None,
        end_date=None,
    ):
        if start_date is None and end_date is None:
            default_date = datetime.now(_REPORT_TIMEZONE).date()
            start_date = default_date
            end_date = default_date
        records = self._filtered_records(
            username=username,
            path=path,
            method=method,
            status=status,
            start_date=start_date,
            end_date=end_date,
            include_anonymous=False,
        )
        users = defaultdict(list)
        endpoints = defaultdict(list)
        days = defaultdict(list)
        day_users = defaultdict(set)
        for record in records:
            user_key = record["username"] or "游客"
            endpoint_key = (record["method"], _endpoint_pattern(record["path"]))
            day_key = record["_timestamp"].date().isoformat()
            users[user_key].append(record)
            endpoints[endpoint_key].append(record)
            days[day_key].append(record)
            day_users[day_key].add(user_key)

        def group_stats(group_records):
            errors = sum(1 for record in group_records if _is_error(record))
            return {
                "requests": len(group_records),
                "errors": errors,
                "error_rate": round(errors / len(group_records) * 100, 1) if group_records else 0,
                **_duration_stats(group_records),
            }

        user_rows = []
        for user_key, group_records in users.items():
            user_rows.append({"username": user_key, **group_stats(group_records)})
        user_rows.sort(key=lambda row: (-row["requests"], row["username"]))

        endpoint_rows = []
        for (endpoint_method, endpoint_path), group_records in endpoints.items():
            endpoint_rows.append(
                {
                    "method": endpoint_method,
                    "path": endpoint_path,
                    **group_stats(group_records),
                }
            )
        endpoint_rows.sort(key=lambda row: (-row["requests"], row["method"], row["path"]))

        daily_rows = []
        for day, group_records in sorted(days.items()):
            daily_rows.append(
                {"date": day, "active_users": len(day_users[day]), **group_stats(group_records)}
            )

        today = datetime.now(_REPORT_TIMEZONE).date()
        today_records = self._filtered_records(
            username=username,
            path=path,
            method=method,
            status=status,
            start_date=today,
            end_date=today,
            include_anonymous=False,
        )
        today_users = defaultdict(list)
        for record in today_records:
            if record["username"]:
                today_users[record["username"]].append(record)
        active_users_today = [
            {"username": username, "requests": len(user_records)}
            for username, user_records in today_users.items()
        ]
        active_users_today.sort(key=lambda row: (-row["requests"], row["username"]))

        overview = group_stats(records)
        overview.update(
            {
                "unique_users": len(users),
                "authenticated_users": sum(1 for username in users if username != "游客"),
                "unique_endpoints": len(endpoints),
                "slow_requests": sum(1 for record in records if record["event"] == "slow"),
                "active_users_today": len(active_users_today),
                "active_users_today_date": today.isoformat(),
                "active_users_today_list": active_users_today,
            }
        )
        return {
            "overview": overview,
            "users": user_rows,
            "endpoints": endpoint_rows,
            "daily": daily_rows,
        }
