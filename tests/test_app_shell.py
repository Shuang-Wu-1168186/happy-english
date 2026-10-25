from tests.conftest import opaque_id, sign_in


def _placement(payload, slot):
    return next(item for item in payload["placements"] if item["slot"] == slot)


def test_app_bootstrap_is_additive_and_uses_typed_actions(client):
    headers = sign_in(client, "learner_test")

    response = client.get(
        "/api/learning/app/bootstrap?platform=android&app_version=1.8.0",
        headers=headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == 1
    assert len(payload["revision"]) == 20
    modules = _placement(payload, "home.modules")["items"]
    assert modules[0]["action"]["type"] == "open_module"
    assert modules[0]["action"]["module_id"].startswith("hei1_")
    vocabulary = next(
        item
        for item in _placement(payload, "learn.collections")["items"]
        if item["id"] == "collection:professional-vocabulary"
    )
    assert vocabulary["action"] == {
        "type": "open_collection",
        "collection_code": "professional-vocabulary",
    }
    assert "action_resolved" in {
        definition["event_name"] for definition in payload["analytics_policy"]["definitions"]
    }

    # The deployed Android client keeps using this endpoint and its original
    # response shape while it has not migrated to Bootstrap.
    legacy = client.get("/api/learning/app/modules", headers=headers)
    assert legacy.status_code == 200
    assert all("action" not in item for item in legacy.json()["items"])


def test_collection_presentation_can_change_without_changing_the_client(client):
    admin_headers = sign_in(client)
    saved = client.post(
        "/api/admin/app-presentation-configs",
        headers=admin_headers,
        json={
            "target_type": "collection",
            "target_key": "professional-vocabulary",
            "platform": "android",
            "layout_code": "content_grid_v1",
            "presentation": {
                "title": "职场词汇",
                "subtitle": "软件、商务和专业沟通表达。",
                "source_resource": "vocabulary",
                "theme": "ink",
            },
            "min_app_version": "1.8.0",
        },
    )
    assert saved.status_code == 201
    assert saved.json()["id"].startswith("hei1_")

    learner_headers = sign_in(client, "learner_test")
    collection = client.get(
        "/api/learning/app/collections/professional-vocabulary?platform=android",
        headers=learner_headers,
    )
    assert collection.status_code == 200
    payload = collection.json()
    assert payload["source_resource"] == "vocabulary"
    assert payload["layout_code"] == "content_grid_v1"
    assert payload["presentation"]["title"] == "职场词汇"
    assert payload["items"][0]["action"]["type"] == "open_content"
    assert payload["items"][0]["action"]["item_id"].startswith("hei1_")


def test_family_owner_can_manage_typed_shortcuts_without_changing_legacy_shortcuts(client):
    owner_headers = sign_in(client, "learner_test")
    group = client.post(
        "/api/learning/family-groups",
        headers=owner_headers,
        json={"name": "埋点测试家庭"},
    )
    assert group.status_code == 201
    group_id = group.json()["id"]

    created = client.post(
        f"/api/learning/family-groups/{group_id}/shortcuts",
        headers=owner_headers,
        json={
            "family_group_id": group_id,
            "title": "专业词汇",
            "target_url": "/learn/vocabulary",
            "description": "工作常用表达",
            "icon": "briefcase",
        },
    )
    assert created.status_code == 201
    shortcut = created.json()
    assert shortcut["action"] == {
        "type": "open_collection",
        "collection_code": "professional-vocabulary",
    }

    listed = client.get(
        f"/api/learning/family-groups/{group_id}/shortcuts",
        headers=owner_headers,
    )
    assert listed.status_code == 200
    assert listed.json()["items"][0]["id"] == shortcut["id"]

    unsupported = client.post(
        f"/api/learning/family-groups/{group_id}/shortcuts",
        headers=owner_headers,
        json={
            "family_group_id": group_id,
            "title": "不支持的入口",
            "target_url": "/future-unregistered-screen",
        },
    )
    assert unsupported.status_code == 422

    removed = client.delete(
        f"/api/learning/family-groups/{group_id}/shortcuts/{shortcut['id']}",
        headers=owner_headers,
    )
    assert removed.status_code == 204
    assert client.get(
        f"/api/learning/family-groups/{group_id}/shortcuts",
        headers=owner_headers,
    ).json()["items"] == []
