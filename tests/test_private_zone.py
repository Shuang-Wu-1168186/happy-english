from tests.conftest import sign_in


def create_family_member(client, admin_headers):
    response = client.post(
        "/api/admin/users",
        headers=admin_headers,
        json={
            "username": "family_test",
            "password": "Testing123!",
            "full_name": "家庭成员",
            "role": "learner",
            "status": "active",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_private_zone_features_and_family_items_are_scoped(client):
    admin_headers = sign_in(client)
    family_member = create_family_member(client, admin_headers)
    textbook = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "material_code": "family-textbook",
            "title": "家庭英语课本",
            "material_type": "textbook",
        },
    )
    assert textbook.status_code == 201
    interview_material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "material_code": "family-interview-practice",
            "title": "家庭面试题练习",
            "material_type": "interview",
        },
    )
    assert interview_material.status_code == 201
    locked_course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "course_code": "family-locked-course",
            "title": "家庭会员课程",
            "access_policy": "benefit",
        },
    )
    assert locked_course.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    group = client.post(
        "/api/learning/family-groups",
        headers=learner_headers,
        json={"name": "我们家"},
    )
    assert group.status_code == 201
    group_id = group.json()["id"]

    invite = client.post(
        f"/api/learning/family-groups/{group_id}/invite-code",
        headers=learner_headers,
    )
    assert invite.status_code == 200
    family_member_headers = sign_in(client, family_member["username"])
    add_member = client.post(
        "/api/learning/family-groups/join",
        headers=family_member_headers,
        json={"invite_code": invite.json()["invite_code"]},
    )
    assert add_member.status_code == 200
    assert len(add_member.json()["members"]) == 2
    learner_headers = sign_in(client, "learner_test")

    for resource_type, resource_id in (
        ("material", textbook.json()["id"]),
        ("course", locked_course.json()["id"]),
    ):
        saved = client.post(
            "/api/learning/private-zone/items",
            headers=learner_headers,
            json={
                "scope_type": "family",
                "family_group_id": group_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
            },
        )
        assert saved.status_code == 201
        assert saved.json()["source"]["label"] == "家庭"

    saved_items = client.get("/api/learning/private-zone/items", headers=learner_headers)
    assert saved_items.status_code == 200
    saved_by_type = {
        item["resource"]["resource_type"]: item for item in saved_items.json()["items"]
    }
    assert saved_by_type["material"]["feature"]["feature_code"] == "my-textbooks"
    assert saved_by_type["course"]["access"]["access_state"] == "locked"

    interview_item = client.post(
        "/api/learning/private-zone/items",
        headers=learner_headers,
        json={
            "scope_type": "personal",
            "resource_type": "material",
            "resource_id": interview_material.json()["id"],
        },
    )
    assert interview_item.status_code == 201
    assert interview_item.json()["feature"]["feature_code"] == "my-interview-questions"

    personal_note = client.post(
        "/api/learning/private-zone/notes",
        headers=learner_headers,
        json={
            "note_date": "2026-10-09",
            "title": "我的笔记",
            "scope_type": "personal",
        },
    )
    assert personal_note.status_code == 201
    personal_note_id = personal_note.json()["note"]["id"]

    family_note = client.post(
        "/api/learning/private-zone/notes",
        headers=learner_headers,
        json={
            "note_date": "2026-10-09",
            "title": "家庭共学笔记",
            "scope_type": "family",
            "family_group_id": group_id,
        },
    )
    assert family_note.status_code == 201
    family_note_id = family_note.json()["note"]["id"]

    personal_item = client.post(
        "/api/learning/private-zone/items",
        headers=learner_headers,
        json={
            "scope_type": "personal",
            "resource_type": "note",
            "resource_id": personal_note_id,
        },
    )
    assert personal_item.status_code == 409

    home = client.get("/api/learning/private-zone", headers=learner_headers)
    assert home.status_code == 200
    assert {item["source"]["label"] for item in home.json()["items"]} == {"个人", "家庭"}
    assert {feature["feature_code"] for feature in home.json()["features"]} >= {
        "my-english-notes",
        "my-textbooks",
        "textbook-vocabulary",
        "my-interview-questions",
    }
    assert "saved-learning" not in {
        feature["feature_code"] for feature in home.json()["features"]
    }
    assert home.json()["public_entries"] == []

    member_headers = sign_in(client, "family_test")
    member_home = client.get("/api/learning/private-zone", headers=member_headers)
    assert member_home.status_code == 200
    member_note_ids = {
        item["resource"]["id"]
        for item in member_home.json()["items"]
        if item["resource"]["resource_type"] == "note"
    }
    assert family_note_id in member_note_ids
    assert personal_note_id not in member_note_ids

    public_notes = client.get("/api/content/notes", headers=member_headers)
    assert public_notes.status_code == 200
    assert personal_note_id not in {item["id"] for item in public_notes.json()["items"]}


def test_only_family_creator_can_rename_a_family_group(client):
    admin_headers = sign_in(client)
    family_member = create_family_member(client, admin_headers)
    owner_headers = sign_in(client, "learner_test")
    created = client.post(
        "/api/learning/family-groups",
        headers=owner_headers,
        json={"name": "周末英语小组"},
    )
    assert created.status_code == 201
    group_id = created.json()["id"]

    added_member = client.post(
        f"/api/learning/family-groups/{group_id}/members",
        headers=owner_headers,
        json={"username": family_member["username"], "role": "admin"},
    )
    assert added_member.status_code == 200

    owner_headers = sign_in(client, "learner_test")
    renamed = client.put(
        f"/api/learning/family-groups/{group_id}",
        headers=owner_headers,
        json={"name": "周末快乐英语"},
    )
    assert renamed.status_code == 200
    assert renamed.json()["name"] == "周末快乐英语"

    member_headers = sign_in(client, family_member["username"])
    forbidden = client.put(
        f"/api/learning/family-groups/{group_id}",
        headers=member_headers,
        json={"name": "管理员不能改名"},
    )
    assert forbidden.status_code == 403

    owner_headers = sign_in(client, "learner_test")
    groups = client.get("/api/learning/family-groups", headers=owner_headers)
    assert groups.status_code == 200
    assert groups.json()["items"][0]["name"] == "周末快乐英语"


def test_private_zone_feature_config_is_admin_only(client):
    learner_headers = sign_in(client, "learner_test")
    forbidden = client.get("/api/admin/private-zone/features", headers=learner_headers)
    assert forbidden.status_code == 403
    forbidden_shortcuts = client.get(
        "/api/admin/private-zone/shortcuts", headers=learner_headers
    )
    assert forbidden_shortcuts.status_code == 403

    admin_headers = sign_in(client)
    features = client.get("/api/admin/private-zone/features", headers=admin_headers)
    assert features.status_code == 200
    assert any(item["feature_code"] == "my-textbooks" for item in features.json()["items"])

    updated = client.put(
        "/api/admin/private-zone/features/my-textbooks",
        headers=admin_headers,
        json={
            "title": "我的课本收藏",
            "title_en": "My Textbooks",
            "description": "收藏课本。",
            "route_key": "private-textbooks",
            "target_url": "/learning-materials/1",
            "config": {"resource_types": ["material"], "material_types": ["textbook"]},
            "sort_order": 15,
            "is_enabled": 1,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "我的课本收藏"
    assert updated.json()["target_url"] == "/learning-materials/1"
    assert updated.json()["config"]["material_types"] == ["textbook"]

    created = client.post(
        "/api/admin/private-zone/features",
        headers=admin_headers,
        json={
            "title": "公共数学练习",
            "title_en": "Public Math Practice",
            "description": "所有学习者都可以打开。",
            "icon": "➗",
            "route_key": "public-entry",
            "target_url": "/learn/math-cards",
            "config": {},
            "sort_order": 50,
            "is_enabled": 1,
        },
    )
    assert created.status_code == 201
    assert created.json()["feature_code"].startswith("public-")
    assert created.json()["target_url"] == "/learn/math-cards"


def test_private_zone_personal_tools_and_admin_shortcuts_are_family_shared(client):
    admin_headers = sign_in(client)
    other_user = create_family_member(client, admin_headers)
    family = client.post(
        "/api/learning/family-groups",
        headers=admin_headers,
        json={"name": "快捷入口家庭"},
    )
    assert family.status_code == 201
    family_group_id = family.json()["id"]
    invite = client.post(
        f"/api/learning/family-groups/{family_group_id}/invite-code",
        headers=admin_headers,
    )
    assert invite.status_code == 200
    other_headers = sign_in(client, other_user["username"])
    joined = client.post(
        "/api/learning/family-groups/join",
        headers=other_headers,
        json={"invite_code": invite.json()["invite_code"]},
    )
    assert joined.status_code == 200
    admin_headers = sign_in(client)
    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "course_code": "personal-tools-course",
            "title": "我收藏的课程",
            "access_policy": "free",
        },
    )
    assert course.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    member_only_family = client.post(
        "/api/learning/family-groups",
        headers=learner_headers,
        json={"name": "只读家庭"},
    )
    assert member_only_family.status_code == 201
    added_admin = client.post(
        f"/api/learning/family-groups/{member_only_family.json()['id']}/members",
        headers=learner_headers,
        json={"username": "admin_test", "role": "member"},
    )
    assert added_admin.status_code == 200
    admin_headers = sign_in(client)
    member_shortcut = client.post(
        "/api/admin/private-zone/shortcuts",
        headers=admin_headers,
        json={
            "family_group_id": member_only_family.json()["id"],
            "title": "成员不能配置",
            "target_url": "/foundation",
        },
    )
    assert member_shortcut.status_code == 403

    invalid_shortcut = client.post(
        "/api/admin/private-zone/shortcuts",
        headers=admin_headers,
        json={
            "family_group_id": family_group_id,
            "title": "不安全链接",
            "target_url": "javascript:alert(1)",
        },
    )
    assert invalid_shortcut.status_code == 422

    shortcut = client.post(
        "/api/admin/private-zone/shortcuts",
        headers=admin_headers,
        json={
            "family_group_id": family_group_id,
            "title": "我的英语教材",
            "target_url": "/foundation",
            "description": "继续自然拼读。",
            "icon": "📚",
            "sort_order": 20,
        },
    )
    assert shortcut.status_code == 201
    shortcut_id = shortcut.json()["id"]
    assert shortcut.json()["scope_type"] == "family"
    assert shortcut.json()["family_group_id"] == family_group_id
    assert shortcut.json()["source"]["family_group_name"] == "快捷入口家庭"

    learner_headers = sign_in(client, "learner_test")
    saved = client.post(
        "/api/learning/private-zone/items",
        headers=learner_headers,
        json={
            "scope_type": "personal",
            "resource_type": "course",
            "resource_id": course.json()["id"],
        },
    )
    assert saved.status_code == 201

    favorite_courses = client.get(
        "/api/learning/private-zone/favorite-courses", headers=learner_headers
    )
    assert favorite_courses.status_code == 200
    assert [item["resource"]["title"] for item in favorite_courses.json()["items"]] == [
        "我收藏的课程"
    ]
    assert favorite_courses.json()["items"][0]["source"]["label"] == "个人"

    learner_shortcut_write = client.post(
        "/api/learning/private-zone/shortcuts",
        headers=learner_headers,
        json={"title": "学习者不能新增", "target_url": "/foundation"},
    )
    assert learner_shortcut_write.status_code == 405

    personal_note = client.post(
        "/api/learning/private-zone/personal-notes",
        headers=learner_headers,
        json={
            "title": "周末学习计划",
            "content": "周六复习课本，周日写三句话。",
            "tags": "计划,英语",
            "color": "yellow",
            "is_pinned": 1,
        },
    )
    assert personal_note.status_code == 201
    note_id = personal_note.json()["id"]

    home = client.get("/api/learning/private-zone", headers=learner_headers)
    assert home.status_code == 200
    assert home.json()["favorite_course_count"] == 1
    assert home.json()["personal_note_count"] == 1
    assert home.json()["shortcuts"] == []
    assert home.json()["public_entries"] == []
    assert home.json()["recent_personal_notes"][0]["title"] == "周末学习计划"

    public_notes = client.get("/api/content/notes", headers=learner_headers)
    assert public_notes.status_code == 200
    assert "周末学习计划" not in {
        item["title"] for item in public_notes.json()["items"]
    }

    other_headers = sign_in(client, other_user["username"])
    other_shortcuts = client.get(
        "/api/learning/private-zone/shortcuts", headers=other_headers
    )
    assert [item["target_url"] for item in other_shortcuts.json()["items"]] == [
        "/foundation"
    ]
    assert other_shortcuts.json()["items"][0]["source"] == {
        "scope_type": "family",
        "label": "来自家庭",
        "family_group_id": family_group_id,
        "family_group_name": "快捷入口家庭",
    }
    assert (
        client.get("/api/learning/private-zone/personal-notes", headers=other_headers)
        .json()["items"]
        == []
    )
    assert client.put(
        f"/api/admin/private-zone/shortcuts/{shortcut_id}",
        headers=other_headers,
        json={
            "family_group_id": family_group_id,
            "title": "越权",
            "target_url": "/",
        },
    ).status_code == 403
    assert client.get(
        f"/api/learning/private-zone/personal-notes/{note_id}", headers=other_headers
    ).status_code == 404

    learner_headers = sign_in(client, "learner_test")
    updated_note = client.put(
        f"/api/learning/private-zone/personal-notes/{note_id}",
        headers=learner_headers,
        json={
            "title": "周末学习计划（已完成）",
            "content": "已经复习课本。",
            "tags": "计划",
            "color": "green",
            "is_pinned": 0,
        },
    )
    assert updated_note.status_code == 200
    assert updated_note.json()["title"] == "周末学习计划（已完成）"
    admin_headers = sign_in(client)
    admin_shortcuts = client.get(
        "/api/learning/private-zone/shortcuts", headers=admin_headers
    )
    assert [item["target_url"] for item in admin_shortcuts.json()["items"]] == [
        "/foundation"
    ]
    updated_shortcut = client.put(
        f"/api/admin/private-zone/shortcuts/{shortcut_id}",
        headers=admin_headers,
        json={
            "family_group_id": family_group_id,
            "title": "我的英语教材",
            "target_url": "/foundation",
            "description": "继续自然拼读。",
            "icon": "📚",
            "sort_order": 20,
        },
    )
    assert updated_shortcut.status_code == 200
    assert updated_shortcut.json()["title"] == "我的英语教材"
    assert client.delete(
        f"/api/admin/private-zone/shortcuts/{shortcut_id}", headers=admin_headers
    ).status_code == 204
    other_headers = sign_in(client, other_user["username"])
    assert client.get(
        "/api/learning/private-zone/shortcuts", headers=other_headers
    ).json()["items"] == []
    learner_headers = sign_in(client, "learner_test")
    assert client.delete(
        f"/api/learning/private-zone/personal-notes/{note_id}", headers=learner_headers
    ).status_code == 204
    assert client.get(
        "/api/learning/private-zone/shortcuts", headers=learner_headers
    ).json()["items"] == []
    assert client.get(
        "/api/learning/private-zone/personal-notes", headers=learner_headers
    ).json()["items"] == []
