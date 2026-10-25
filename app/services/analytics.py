"""Schema-validated analytics with a small, privacy-preserving event vocabulary."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException

from app import schemas as s
from app.dao.analytics import AnalyticsEventDAO, AnalyticsEventDefinitionDAO


BUILTIN_EVENT_DEFINITIONS = {
    "screen_view": {
        "description": "A registered application screen became visible.",
        "allowed_properties": ("tab",),
        "sample_rate": 100,
    },
    "card_impression": {
        "description": "A configured card was visible to the learner.",
        "allowed_properties": ("position",),
        "sample_rate": 100,
    },
    "card_click": {
        "description": "A configured card was selected.",
        "allowed_properties": ("position", "action_type"),
        "sample_rate": 100,
    },
    "action_resolved": {
        "description": "A typed UI action was resolved successfully.",
        "allowed_properties": ("action_type",),
        "sample_rate": 100,
    },
    "action_failed": {
        "description": "A typed UI action could not be opened.",
        "allowed_properties": ("action_type", "reason_code"),
        "sample_rate": 100,
    },
    "content_opened": {
        "description": "A collection item or learning resource was opened.",
        "allowed_properties": ("content_kind",),
        "sample_rate": 100,
    },
    "lesson_started": {
        "description": "A learner started a lesson.",
        "allowed_properties": ("renderer",),
        "sample_rate": 100,
    },
    "lesson_completed": {
        "description": "A learner completed a lesson.",
        "allowed_properties": ("renderer", "elapsed_seconds"),
        "sample_rate": 100,
    },
    "review_answered": {
        "description": "A learner answered a review prompt.",
        "allowed_properties": ("is_correct",),
        "sample_rate": 100,
    },
    "membership_prompt_viewed": {
        "description": "A membership access prompt was displayed.",
        "allowed_properties": ("reason_code",),
        "sample_rate": 100,
    },
    "membership_cta_clicked": {
        "description": "A learner selected a membership call to action.",
        "allowed_properties": ("reason_code",),
        "sample_rate": 100,
    },
}


class AnalyticsService:
    """Own event validation and persistence without accepting free-form data."""

    def __init__(self, db):
        self.db = db
        self.definitions = AnalyticsEventDefinitionDAO(db)
        self.events = AnalyticsEventDAO(db)

    @staticmethod
    def _decode_properties(value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except (TypeError, ValueError):
                value = []
        return list(value) if isinstance(value, list) else []

    @staticmethod
    def _definition_view(row):
        return {
            **dict(row),
            "allowed_properties": AnalyticsService._decode_properties(
                row.get("allowed_properties_json")
            ),
        }

    def _custom_definitions(self):
        return {
            row["event_name"]: self._definition_view(row)
            for row in self.definitions.list_active()
        }

    def _definition_for(self, event_name, custom_definitions):
        if event_name in BUILTIN_EVENT_DEFINITIONS:
            return BUILTIN_EVENT_DEFINITIONS[event_name]
        definition = custom_definitions.get(event_name)
        if not definition:
            raise HTTPException(422, "Unknown or inactive analytics event.")
        return definition

    @staticmethod
    def _assert_fresh(occurred_at):
        now = datetime.now(UTC)
        timestamp = occurred_at if occurred_at.tzinfo else occurred_at.replace(tzinfo=UTC)
        if timestamp > now + timedelta(hours=24) or timestamp < now - timedelta(days=31):
            raise HTTPException(422, "Analytics event timestamp is outside the accepted window.")
        return timestamp.astimezone(UTC).replace(tzinfo=None)

    @staticmethod
    def _assert_allowed_properties(event, definition):
        allowed = set(definition.get("allowed_properties", ()))
        unknown = set(event.properties) - allowed
        if unknown:
            raise HTTPException(
                422,
                f"Analytics properties are not registered for {event.event_name}: {', '.join(sorted(unknown))}.",
            )

    def policy(self):
        custom = self._custom_definitions()
        definitions = []
        for event_name, definition in BUILTIN_EVENT_DEFINITIONS.items():
            definitions.append(
                {
                    "event_name": event_name,
                    "description": definition["description"],
                    "allowed_properties": list(definition["allowed_properties"]),
                    "sample_rate": definition["sample_rate"],
                }
            )
        for event_name, definition in custom.items():
            definitions.append(
                {
                    "event_name": event_name,
                    "description": definition.get("description") or "",
                    "allowed_properties": definition["allowed_properties"],
                    "sample_rate": definition.get("sample_rate", 100),
                }
            )
        return {
            "version": 1,
            "batch_endpoint": "/api/analytics/events:batch",
            "max_batch_size": 100,
            "definitions": definitions,
        }

    def record_batch(self, payload: s.AnalyticsEventBatchInput, user):
        custom = self._custom_definitions()
        prepared = []
        for event in payload.events:
            definition = self._definition_for(event.event_name, custom)
            self._assert_allowed_properties(event, definition)
            source = event.source
            subject = event.subject
            prepared.append(
                {
                    "event_id": str(event.event_id),
                    "user_id": user["id"],
                    "event_name": event.event_name,
                    "occurred_at": self._assert_fresh(event.occurred_at),
                    "session_id": event.session_id or None,
                    "subject_type": subject.subject_type if subject else None,
                    "subject_key": subject.subject_key if subject else None,
                    "source_screen": source.screen if source and source.screen else None,
                    "source_placement": source.placement if source and source.placement else None,
                    "source_item_key": source.item_key if source and source.item_key else None,
                    "properties_json": json.dumps(event.properties, ensure_ascii=False, separators=(",", ":")),
                    "context_json": json.dumps(
                        event.context.model_dump(), ensure_ascii=False, separators=(",", ":")
                    ),
                }
            )

        accepted = sum(self.events.insert_if_absent(event) for event in prepared)
        self.db.commit()
        return {"accepted": accepted, "duplicate": len(prepared) - accepted}

    def list_definitions(self):
        return {"items": [self._definition_view(row) for row in self.definitions.list_all()]}

    def save_definition(self, payload: s.AnalyticsEventDefinitionInput, actor, event_name=None):
        if payload.event_name in BUILTIN_EVENT_DEFINITIONS:
            raise HTTPException(409, "Built-in analytics event definitions cannot be replaced.")
        if event_name is not None and event_name != payload.event_name:
            raise HTTPException(422, "The event name cannot be changed.")
        existing = self.definitions.by_name(payload.event_name)
        if event_name is None and existing:
            raise HTTPException(409, "Analytics event definition already exists.")
        if event_name is not None and not existing:
            raise HTTPException(404, "Analytics event definition not found.")

        values = {
            "event_name": payload.event_name,
            "description": payload.description or None,
            "allowed_properties_json": json.dumps(payload.allowed_properties, ensure_ascii=False),
            "sample_rate": payload.sample_rate,
            "status": payload.status,
            "updated_by": actor["id"],
        }
        if existing:
            self.definitions.update(existing["id"], values)
            definition_id = existing["id"]
        else:
            definition_id = self.definitions.insert({**values, "created_by": actor["id"]})
        self.db.commit()
        return self._definition_view(self.definitions.find_by_id(definition_id))


ANALYTICS_TABLE_SERVICE_TYPES = {
    "analytics_event_definition": AnalyticsService,
    "analytics_event": AnalyticsService,
}
