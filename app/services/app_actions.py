"""Stable, client-facing actions for server-authored application entry points.

Existing Android clients still consume ``target_url`` values.  This module
provides an additive typed representation for new clients and for the app
bootstrap endpoint; it deliberately does not change legacy URL behaviour.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit


COLLECTION_TARGETS = {
    "/learn/notes": "notes",
    "/learn/kids-cards": "kids-cards",
    "/course-resources/kids-cards": "kids-cards",
    "/learn/textbook": "textbook",
    "/course-resources/textbook": "textbook",
    "/learn/math-cards": "math-cards",
    "/course-resources/math-cards": "math-cards",
    "/learn/vocabulary": "professional-vocabulary",
    "/learn/interviews": "interviews",
    "/foundation": "phonics",
}

SUPPORTED_ACTION_TYPES = frozenset(
    {
        "open_home",
        "open_explore",
        "open_module",
        "open_topic",
        "open_course",
        "open_material",
        "open_lesson",
        "open_collection",
        "open_content",
        "open_training",
        "open_podcast",
        "open_private_zone",
        "open_favorite_courses",
        "open_personal_notes",
        "open_web",
    }
)

_MATERIAL_PATH = re.compile(r"^/learning-materials/([^/]+)$")
_COURSE_PATH = re.compile(r"^/courses/([^/]+)$")
_MODULE_PATH = re.compile(r"^/learning/modules/([^/]+)$")
_TOPIC_PATH = re.compile(r"^/learning/topics/([^/]+)$")


def _identifier(value: str) -> int | str | None:
    """Keep opaque IDs intact while converting legacy numeric IDs for routing."""

    value = value.strip()
    if value.isdecimal() and int(value) > 0:
        return int(value)
    if value.startswith("hei1_"):
        return value
    return None


def action_for_target_url(target_url: object) -> dict[str, Any] | None:
    """Translate a supported legacy target URL into a typed action.

    Returning ``None`` is intentional: a new client can present a recoverable
    unavailable state instead of pretending every arbitrary internal path is
    supported.  Existing clients continue to receive and process target URLs.
    """

    if not isinstance(target_url, str) or not target_url.strip():
        return None
    target_url = target_url.strip()
    parsed = urlsplit(target_url)
    # New typed actions only allow HTTPS.  Legacy clients keep receiving their
    # original target_url, so declining an old HTTP link here is non-breaking.
    if parsed.scheme == "https" and parsed.netloc:
        return {"type": "open_web", "url": target_url}
    if parsed.scheme or parsed.netloc:
        return None

    path = parsed.path.rstrip("/") or "/"
    if path == "/private-zone":
        return {"type": "open_private_zone"}
    if path == "/private-zone/favorite-courses":
        return {"type": "open_favorite_courses"}
    if path == "/private-zone/personal-notes":
        return {"type": "open_personal_notes"}
    if collection_code := COLLECTION_TARGETS.get(path):
        return {"type": "open_collection", "collection_code": collection_code}

    for matcher, action_type, identifier_key in (
        (_MATERIAL_PATH, "open_material", "material_id"),
        (_COURSE_PATH, "open_course", "course_id"),
        (_MODULE_PATH, "open_module", "module_id"),
        (_TOPIC_PATH, "open_topic", "topic_id"),
    ):
        match = matcher.match(path)
        if match and (identifier := _identifier(match.group(1))) is not None:
            return {"type": action_type, identifier_key: identifier}
    return None


def action_for_content(resource: str, item_id: int | str) -> dict[str, Any]:
    """Create the one generic content-detail action used by collections."""

    return {"type": "open_content", "resource": resource, "item_id": item_id}


def is_supported_action(action: object) -> bool:
    """Validate configured fallbacks without accepting executable navigation."""

    if not isinstance(action, dict) or action.get("type") not in SUPPORTED_ACTION_TYPES:
        return False
    action_type = action["type"]
    required_key = {
        "open_module": "module_id",
        "open_topic": "topic_id",
        "open_course": "course_id",
        "open_material": "material_id",
        "open_lesson": "lesson_id",
        "open_collection": "collection_code",
        "open_content": "item_id",
        "open_training": "training_id",
        "open_podcast": "podcast_id",
        "open_web": "url",
    }.get(action_type)
    if required_key and not action.get(required_key):
        return False
    if action_type == "open_content" and not action.get("resource"):
        return False
    if action_type == "open_web":
        parsed = urlsplit(str(action["url"]))
        return parsed.scheme == "https" and bool(parsed.netloc)
    return True
