from tests.conftest import sign_in


def create_course(client, headers):
    module = next(
        item
        for item in client.get("/api/learning/modules").json()["items"]
        if item["module_code"] == "elementary-english"
    )
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": module["id"],
            "topic_code": "progress-test-topic",
            "title": "学习进度测试主题",
        },
    )
    assert topic.status_code == 201
    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic.json()["id"],
            "course_code": "progress-test-course",
            "title": "学习进度测试课程",
            "course_type": "dialogue",
            "content_resource": "dialogues",
            "content_reference_id": 1,
            "content": {"blocks": [{"key": "dialogue-1"}, {"key": "dialogue-2"}]},
        },
    )
    assert course.status_code == 201
    return course.json()["id"]


def test_course_progress_tracks_items_and_resume_position(client):
    course_id = create_course(client, sign_in(client))
    headers = sign_in(client, "learner_test")

    saved = client.post(
        "/api/learning/progress",
        headers=headers,
        json={
            "course_id": course_id,
            "total_item_count": 2,
            "last_position_seconds": 35,
            "item": {
                "item_key": "dialogue-1",
                "item_type": "dialogue",
                "is_completed": True,
                "last_position_seconds": 35,
            },
        },
    )

    assert saved.status_code == 200
    assert saved.json()["completed_item_count"] == 1
    assert saved.json()["progress_percent"] == 50.0
    assert saved.json()["last_item_key"] == "dialogue-1"
    assert saved.json()["last_position_seconds"] == 35
    assert saved.json()["course"]["id"] == course_id

    records = client.get("/api/learning/progress", headers=headers)
    assert records.status_code == 200
    assert records.json()["items"][0]["course_id"] == course_id
    assert records.json()["items"][0]["course_content_resource"] == "dialogues"
    resumed = client.get("/api/learning/progress/continue", headers=headers).json()
    assert resumed["course_id"] == course_id
    assert resumed["course_content_reference_id"] == 1


def test_learning_sessions_accumulate_time_without_duplicate_finish(client):
    course_id = create_course(client, sign_in(client))
    headers = sign_in(client, "learner_test")

    started = client.post(
        "/api/learning/study-sessions",
        headers=headers,
        json={"course_id": course_id, "platform": "mini_program", "entry_source": "home"},
    )
    assert started.status_code == 201
    assert started.json()["reused"] is False
    session_id = started.json()["id"]

    reused = client.post(
        "/api/learning/study-sessions",
        headers=headers,
        json={"course_id": course_id, "platform": "mini_program"},
    )
    assert reused.status_code == 201
    assert reused.json()["id"] == session_id
    assert reused.json()["reused"] is True

    finished = client.put(
        f"/api/learning/study-sessions/{session_id}/finish",
        headers=headers,
        json={"active_seconds": 1},
    )
    assert finished.status_code == 200
    assert finished.json()["active_seconds"] == 1
    assert finished.json()["ended_at"]
    assert (
        client.put(
            f"/api/learning/study-sessions/{session_id}/finish",
            headers=headers,
            json={"active_seconds": 100},
        ).json()["active_seconds"]
        == 1
    )

    summary = client.get("/api/learning/study-time", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_active_seconds"] == 1
    assert summary.json()["days"][0]["session_count"] == 1
