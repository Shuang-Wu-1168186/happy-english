from datetime import UTC, datetime

from sqlalchemy import select

from app import models as m
from tests.conftest import sign_in


def _event(*, event_id, event_name="action_resolved", properties=None):
    return {
        "event_id": event_id,
        "event_name": event_name,
        "occurred_at": datetime.now(UTC).isoformat(),
        "session_id": "analytics-test-session",
        "subject": {
            "subject_type": "collection",
            "subject_key": "professional-vocabulary",
        },
        "source": {
            "screen": "private_zone",
            "placement": "private_zone.shortcuts",
            "item_key": "professional-vocabulary",
        },
        "context": {
            "platform": "android",
            "app_version": "1.8.0",
            "bootstrap_revision": "test-revision",
            "renderer": "shortcut_grid_v1",
        },
        "properties": properties or {"action_type": "open_collection"},
    }


def test_analytics_policy_and_batch_are_validated_and_idempotent(client):
    headers = sign_in(client, "learner_test")
    policy = client.get("/api/analytics/policy", headers=headers)
    assert policy.status_code == 200
    assert policy.json()["batch_endpoint"] == "/api/analytics/events:batch"
    assert any(item["event_name"] == "lesson_completed" for item in policy.json()["definitions"])

    event = _event(event_id="e4a57c9d-487b-4bf6-a259-a5328fa4cba7")
    first = client.post("/api/analytics/events:batch", headers=headers, json={"events": [event]})
    assert first.status_code == 202
    assert first.json() == {"accepted": 1, "duplicate": 0}

    retry = client.post("/api/analytics/events:batch", headers=headers, json={"events": [event]})
    assert retry.status_code == 202
    assert retry.json() == {"accepted": 0, "duplicate": 1}
    with client.app.state.engine.connect() as connection:
        rows = connection.execute(select(m.analytics_event)).mappings().all()
    assert len(rows) == 1
    assert rows[0]["event_name"] == "action_resolved"
    assert '{"action_type":"open_collection"}' == rows[0]["properties_json"]

    sensitive = _event(
        event_id="1ae19d48-8c62-4db6-9d67-b5d3db2c6974",
        properties={"raw_text": "do not store this"},
    )
    assert client.post(
        "/api/analytics/events:batch", headers=headers, json={"events": [sensitive]}
    ).status_code == 422

    unknown = _event(
        event_id="e9ff6f87-bf26-4b46-ad2f-b69228d19e36",
        event_name="unregistered_event",
        properties={},
    )
    assert client.post(
        "/api/analytics/events:batch", headers=headers, json={"events": [unknown]}
    ).status_code == 422


def test_admin_can_register_a_future_event_without_a_client_release(client):
    admin_headers = sign_in(client)
    definition = client.post(
        "/api/admin/analytics/event-definitions",
        headers=admin_headers,
        json={
            "event_name": "exercise_submitted",
            "description": "A configured exercise was submitted.",
            "allowed_properties": ["exercise_kind"],
            "sample_rate": 50,
        },
    )
    assert definition.status_code == 201
    assert definition.json()["id"].startswith("hei1_")

    learner_headers = sign_in(client, "learner_test")
    event = _event(
        event_id="d15ee86f-d509-4cf3-bceb-46c2dd2d4bac",
        event_name="exercise_submitted",
        properties={"exercise_kind": "choice"},
    )
    response = client.post(
        "/api/analytics/events:batch", headers=learner_headers, json={"events": [event]}
    )
    assert response.status_code == 202
    assert response.json() == {"accepted": 1, "duplicate": 0}
