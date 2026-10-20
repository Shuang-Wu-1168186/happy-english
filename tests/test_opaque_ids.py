import pytest

from app.api.opaque_ids import OpaqueIdRoute
from app.core.opaque_ids import OpaqueIdCodec, OpaqueIdError, codec_from_settings
from app.core.security import COOKIE, serializer
from tests.conftest import opaque_id, sign_in


def test_opaque_identifier_codec_is_stable_and_authenticated(client):
    codec = codec_from_settings(client.app.state.settings)

    token = codec.encode(42)

    assert token.startswith("hei1_")
    assert token == codec.encode(42)
    assert codec.decode(token) == 42
    with pytest.raises(OpaqueIdError):
        codec.decode(token[:-1] + ("A" if token[-1] != "A" else "B"))


def test_opaque_identifier_codec_accepts_retiring_rotation_keys():
    retiring = OpaqueIdCodec("retiring-external-id-secret")
    current = OpaqueIdCodec(
        "current-external-id-secret", ("retiring-external-id-secret",)
    )

    assert current.decode(retiring.encode(42)) == 42


def test_every_id_bearing_api_route_uses_the_opaque_id_boundary(client):
    api_routers = [
        route.original_router
        for route in client.app.routes
        if getattr(getattr(route, "include_context", None), "prefix", None) == "/api"
    ]

    assert api_routers
    assert all(router.route_class is OpaqueIdRoute for router in api_routers)


def test_api_externalizes_ids_and_rejects_raw_or_tampered_values(client):
    headers = sign_in(client, "learner_test")
    modules = client.get("/api/learning/modules", headers=headers)

    assert modules.status_code == 200
    module = next(item for item in modules.json()["items"] if item["module_code"] == "beginner-english")
    token = module["id"]
    assert token == opaque_id(client, 1)
    assert isinstance(token, str) and token.startswith("hei1_")

    detail = client.get(f"/api/learning/modules/{token}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == token
    assert all(topic["id"].startswith("hei1_") for topic in detail.json()["topics"])

    assert client.get("/api/learning/modules/1", headers=headers).status_code == 422
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")
    assert client.get(f"/api/learning/modules/{tampered}", headers=headers).status_code == 422


def test_request_body_and_query_identifiers_are_decoded_at_the_api_boundary(client):
    admin_headers = sign_in(client)
    module_id = opaque_id(client, 2)

    created = client.post(
        "/api/admin/learning/topics",
        headers=admin_headers,
        json={
            "module_id": module_id,
            "topic_code": "opaque-id-topic",
            "title": "Opaque ID topic",
        },
    )
    assert created.status_code == 201
    topic_id = created.json()["id"]
    assert topic_id.startswith("hei1_")

    raw_body = client.post(
        "/api/admin/learning/topics",
        headers=admin_headers,
        json={"module_id": 2, "topic_code": "raw-id-topic", "title": "Raw ID topic"},
    )
    assert raw_body.status_code == 422

    queried = client.get(f"/api/learning/courses?topic_id={topic_id}")
    assert queried.status_code == 200
    assert client.get("/api/learning/courses?topic_id=2").status_code == 422


def test_progress_accepts_tokens_and_session_payload_never_contains_a_raw_uid(client):
    headers = sign_in(client, "learner_test")
    sentence = client.get("/api/content/sentences", headers=headers).json()["items"][0]

    saved = client.post(
        "/api/progress",
        headers=headers,
        json={"content_type": "everyday_sentence", "item_id": sentence["id"]},
    )
    assert saved.status_code == 200
    assert saved.json()["success"] is True
    assert client.get("/api/progress", headers=headers).json()[0]["item_id"] == sentence["id"]

    raw_id = client.post(
        "/api/progress",
        headers=headers,
        json={"content_type": "everyday_sentence", "item_id": 1},
    )
    assert raw_id.status_code == 422

    serialized_session = client.cookies.get(COOKIE)
    payload = serializer(client.app.state.settings).loads(serialized_session)
    assert payload["uid"].startswith("hei1_")
    assert payload["uid"] != 2


def test_internal_deep_links_externalize_and_require_opaque_identifiers(client):
    headers = sign_in(client)
    features = client.get("/api/admin/private-zone/features", headers=headers)

    assert features.status_code == 200
    textbooks = next(
        item for item in features.json()["items"] if item["feature_code"] == "my-textbooks"
    )
    opaque_target_url = f"/learning-materials/{opaque_id(client, 1)}"
    assert textbooks["target_url"] == opaque_target_url
    feature_payload = {
        key: textbooks[key]
        for key in (
            "title",
            "title_en",
            "description",
            "icon",
            "route_key",
            "config",
            "sort_order",
            "is_enabled",
        )
    }

    round_tripped = client.put(
        "/api/admin/private-zone/features/my-textbooks",
        headers=headers,
        json={**feature_payload, "target_url": opaque_target_url},
    )
    assert round_tripped.status_code == 200
    assert round_tripped.json()["target_url"] == opaque_target_url

    raw_deep_link = client.put(
        "/api/admin/private-zone/features/my-textbooks",
        headers=headers,
        json={**feature_payload, "target_url": "/learning-materials/1"},
    )
    assert raw_deep_link.status_code == 422
