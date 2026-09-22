from io import BytesIO

import pytest
from PIL import Image

from app.core.security import COOKIE
from tests.conftest import sign_in


def test_health_session_cors_and_csrf(client):
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/health/ready").status_code == 200
    response = client.get("/api/auth/session", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "httponly" in response.headers["set-cookie"].lower()
    assert response.headers["cache-control"] == "no-store"
    assert (
        client.post("/api/auth/login", json={"username": "admin_test", "password": "Testing123!"}).status_code
        == 403
    )
    assert client.get("/api/content/sentences").status_code == 401
    assert (
        "access-control-allow-origin"
        not in client.get("/api/health", headers={"Origin": "https://untrusted.example"}).headers
    )


def test_login_audit_records_ip_time_and_login_outcome(client):
    token = client.get("/api/auth/session").json()["csrf_token"]
    success = client.post(
        "/api/auth/login",
        json={"username": "admin_test", "password": "Testing123!"},
        headers={
            "X-CSRF-Token": token,
            "X-Forwarded-For": "203.0.113.24",
            "User-Agent": "HappyEnglish login audit test",
        },
    )
    assert success.status_code == 200
    failed = client.post(
        "/api/auth/login",
        json={"username": "admin_test", "password": "wrong password"},
        headers={
            "X-CSRF-Token": success.json()["csrf_token"],
            "X-Forwarded-For": "2001:db8::24",
            "User-Agent": "HappyEnglish failed login test",
        },
    )
    assert failed.status_code == 401

    records = client.get("/api/admin/login-audits?q=admin_test").json()["items"]
    succeeded = next(record for record in records if record["success"])
    rejected = next(record for record in records if not record["success"])
    assert succeeded["user_id"] == 1
    assert succeeded["full_name"] == "测试管理员"
    assert succeeded["login_ip"] == "203.0.113.24"
    assert succeeded["user_agent"] == "HappyEnglish login audit test"
    assert succeeded["logged_in_at"]
    assert rejected["user_id"] is None
    assert rejected["login_ip"] == "2001:db8::24"

    sign_in(client, "learner_test")
    assert client.get("/api/admin/login-audits").status_code == 403


@pytest.mark.parametrize(
    "resource",
    [
        "sentences",
        "notes",
        "note-items",
        "vocabulary",
        "interviews",
        "interview-categories",
        "kids-cards",
        "math-cards",
        "textbook",
        "phonics",
        "dialogues",
    ],
)
def test_learning_modules_and_details(client, resource):
    sign_in(client, "learner_test")
    response = client.get(f"/api/content/{resource}")
    assert response.status_code == 200
    assert response.json()["total"] > 0
    detail = client.get(f"/api/content/{resource}/1")
    assert detail.status_code == 200
    if resource == "kids-cards":
        assert detail.json()["examples"][0]["translation"] == "我喜欢苹果。"
    if resource == "phonics":
        assert detail.json()["quiz_choices"] == ["cat", "dog"]
    if resource == "sentences":
        assert detail.json()["next_id"] == 2
    if resource == "textbook":
        assert detail.json()["sentences"][0]["english_text"] == "Hello!"


def test_filter_pagination_and_auth_permissions(client):
    headers = sign_in(client, "learner_test")
    assert client.get("/api/content/sentences?q=Hello").json()["total"] == 1
    page = client.get("/api/content/sentences?page_size=1&page=2").json()
    assert page["items"][0]["id"] == 2
    assert client.get("/api/content/sentences?page=0").status_code == 422
    assert client.get("/api/admin/users").status_code == 403
    assert (
        client.post("/api/content/sentences", headers=headers, json={"en": "No", "cn": "不"}).status_code
        == 403
    )
    assert client.get("/api/content/user").status_code == 404


def test_admin_crud_validation_and_delete(client):
    headers = sign_in(client)
    payload = {"en": "Thank you.", "cn": "谢谢。", "tag": "Greetings"}
    created = client.post("/api/content/sentences", headers=headers, json=payload)
    assert created.status_code == 201
    item_id = created.json()["id"]
    updated = client.put(
        f"/api/content/sentences/{item_id}", headers=headers, json={**payload, "cn": "谢谢你。"}
    )
    assert updated.json()["cn"] == "谢谢你。"
    assert client.post("/api/content/note-items", headers=headers, json={}).status_code == 422
    assert client.delete(f"/api/content/sentences/{item_id}", headers=headers).status_code == 204
    assert client.get(f"/api/content/sentences/{item_id}").status_code == 404


def test_new_note_items_append_to_the_note(client):
    headers = sign_in(client)
    payload = {
        "note_id": 1,
        "item_type": "vocab",
        "item_title": "first new card",
        "raw_text": "first new card",
        "english_text": "first new card",
        "chinese_text": "第一张新卡片",
    }
    first = client.post("/api/content/note-items", headers=headers, json=payload)
    second = client.post(
        "/api/content/note-items",
        headers=headers,
        json={**payload, "item_title": "second new card", "raw_text": "second new card"},
    )
    assert first.status_code == second.status_code == 201
    assert first.json()["item_order"] == 1
    assert second.json()["item_order"] == 2
    items = client.get("/api/content/notes/1").json()["items"]
    assert [item["item_title"] for item in items][-2:] == ["first new card", "second new card"]


def test_interview_children_replaced_in_transaction(client):
    headers = sign_in(client)
    payload = {
        "category_id": 1,
        "question": "A new question",
        "sections": [
            {"section_type": "situation", "section_title": "Situation", "content_en": "I worked in a team."}
        ],
    }
    response = client.post("/api/content/interviews", headers=headers, json=payload)
    assert response.status_code == 201
    item_id = response.json()["id"]
    assert len(response.json()["sections"]) == 1
    response = client.put(
        f"/api/content/interviews/{item_id}", headers=headers, json={**payload, "sections": []}
    )
    assert response.json()["sections"] == []
    assert client.delete(f"/api/content/interviews/{item_id}", headers=headers).status_code == 204


def test_progress_is_per_user_and_checks_note_parent(client):
    headers = sign_in(client, "learner_test")
    payload = {"content_type": "everyday_sentence", "item_id": 1}
    assert client.post("/api/progress", headers=headers, json=payload).status_code == 200
    assert (
        client.post(
            "/api/progress", headers=headers, json={**payload, "item_id": 2, "completed": True}
        ).status_code
        == 200
    )
    records = client.get("/api/progress").json()
    assert len(records) == 1 and records[0]["completed"] == 1 and records[0]["item_id"] == 2
    assert (
        client.post(
            "/api/progress",
            headers=headers,
            json={"content_type": "english_note", "parent_id": 999, "item_id": 1},
        ).status_code
        == 404
    )
    sign_in(client)
    assert client.get("/api/progress").json() == []


def test_signup_profile_password_revokes_old_cookie(client):
    token = client.get("/api/auth/session").json()["csrf_token"]
    data = {"username": "new_user", "full_name": "New User", "password": "Newpassword123!"}
    headers = {"X-CSRF-Token": token}
    assert client.post("/api/auth/signup", json={**data, "role": "admin"}, headers=headers).status_code == 422
    created = client.post("/api/auth/signup", json=data, headers=headers)
    assert created.status_code == 201 and created.json()["role"] == "learner"
    assert "password_hash" not in created.json()
    assert client.post("/api/auth/signup", json=data, headers=headers).status_code == 409
    headers = sign_in(client)
    old_cookie = client.cookies.get(COOKIE)
    assert client.put("/api/profile", json={"full_name": "Updated"}, headers=headers).status_code == 200
    changed = client.post(
        "/api/profile/password",
        json={"old_password": "Testing123!", "new_password": "Changed123!"},
        headers=headers,
    )
    assert changed.status_code == 200
    client.cookies.clear()
    client.cookies.set(COOKIE, old_cookie)
    assert client.get("/api/content/sentences").status_code == 401


def test_admin_cannot_disable_self_and_inactive_user_loses_access(client):
    headers = sign_in(client)
    payload = {"username": "admin_test", "full_name": "Admin", "role": "admin", "status": "inactive"}
    assert client.put("/api/admin/users/1", json=payload, headers=headers).status_code == 409
    payload.update(username="learner_test", role="learner")
    assert client.put("/api/admin/users/2", json=payload, headers=headers).status_code == 200
    response = client.post(
        "/api/auth/login", json={"username": "learner_test", "password": "Testing123!"}, headers=headers
    )
    assert response.status_code == 401


def test_upload_and_disabled_audio(client):
    headers = sign_in(client)
    assert (
        client.post(
            "/api/uploads", headers=headers, files={"file": ("fake.png", b"not an image", "image/png")}
        ).status_code
        == 400
    )
    data = BytesIO()
    Image.new("RGB", (8, 8), "green").save(data, format="PNG")
    uploaded = client.post(
        "/api/uploads", headers=headers, files={"file": ("real.png", data.getvalue(), "image/png")}
    )
    assert uploaded.status_code == 201
    response = client.get(uploaded.json()["url"])
    assert response.status_code == 200 and response.headers["content-type"] == "image/webp"
    assert client.post("/api/audio/tts", headers=headers, json={"text": "Hello"}).status_code == 503


def test_delete_note_removes_children_and_progress(client):
    headers = sign_in(client)
    assert (
        client.post(
            "/api/progress",
            headers=headers,
            json={"content_type": "english_note", "parent_id": 1, "item_id": 1},
        ).status_code
        == 200
    )
    assert client.delete("/api/content/notes/1", headers=headers).status_code == 204
    assert client.get("/api/content/note-items/1").status_code == 404
    assert client.get("/api/progress").json() == []
