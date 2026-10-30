from tests.conftest import opaque_id, sign_in
from app.services.progress import StudyProgressService


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
            "content_reference_id": opaque_id(client, 1),
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
    assert resumed["course_content_reference_id"] == opaque_id(client, 1)


def test_completed_courseware_lesson_is_available_for_review(client):
    admin_headers = sign_in(client)
    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": opaque_id(client, 2),
            "material_code": "review-courseware-material",
            "title": "复习课件教材",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201
    material_id = material.json()["id"]
    lesson = client.post(
        f"/api/admin/learning-materials/{material_id}/lessons",
        headers=admin_headers,
        json={
            "lesson_code": "review-courseware-lesson",
            "title": "预订餐厅",
            "lesson_format": "courseware",
        },
    )
    assert lesson.status_code == 201
    lesson_id = lesson.json()["id"]
    hero_payload = {
        "block_code": "hero",
        "block_type": "hero",
        "payload": {
            "phrase": "I'd like to make a reservation.",
            "meaning": "我想预订座位。",
            "memory": "用 make a reservation 表示预订。",
            "key_sentence": {
                "english": "I'd like to make a reservation.",
                "chinese": "我想预订座位。",
            },
        },
    }
    block = client.post(
        f"/api/admin/learning-material-lessons/{lesson_id}/courseware-blocks",
        headers=admin_headers,
        json=hero_payload,
    )
    assert block.status_code == 201
    assert client.put(
        f"/api/admin/courseware-blocks/{block.json()['id']}/sources",
        headers=admin_headers,
        json={
            "items": [
                {
                    "source_resource": "english_note_item",
                    "source_reference_id": opaque_id(client, 1),
                    "source_field": "english_text",
                    "source_snapshot_text": "Good morning",
                }
            ]
        },
    ).status_code == 200
    assert client.put(
        f"/api/admin/courseware-blocks/{block.json()['id']}",
        headers=admin_headers,
        json={**hero_payload, "status": "published"},
    ).status_code == 200
    assert client.put(
        f"/api/admin/learning-material-lessons/{lesson_id}",
        headers=admin_headers,
        json={
            "lesson_code": "review-courseware-lesson",
            "title": "预订餐厅",
            "lesson_format": "courseware",
            "is_published": 1,
        },
    ).status_code == 200
    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": opaque_id(client, 2),
            "material_id": material_id,
            "course_code": "review-courseware-course",
            "title": "餐厅英语",
        },
    )
    assert course.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    saved = client.post(
        "/api/learning/progress",
        headers=learner_headers,
        json={
            "course_id": course.json()["id"],
            "total_item_count": 1,
            "item": {
                "item_key": f"lesson-{lesson_id}",
                "item_type": "material_lesson",
                "item_reference_id": lesson_id,
                "is_completed": True,
            },
        },
    )
    assert saved.status_code == 200

    review = client.get("/api/learning/review-items?days=7&limit=10", headers=learner_headers)
    assert review.status_code == 200
    course_item = next(item for item in review.json()["items"] if item["resource"] == "course-lessons")
    assert course_item["label"] == "课程复习 · 餐厅英语"
    assert course_item["prompt"] == "I'd like to make a reservation."
    assert course_item["answer"] == "我想预订座位。"


def test_structured_lesson_review_uses_a_published_dialogue_turn():
    class Result:
        def mappings(self):
            return [
                {
                    "payload_json": (
                        '{"turns":[{"english":"What size are you?",'
                        '"chinese":"你穿什么尺码？"}]}'
                    )
                }
            ]

    class Database:
        def execute(self, _statement):
            return Result()

    assert StudyProgressService(Database())._structured_lesson_review_pair(1) == (
        "What size are you?",
        "你穿什么尺码？",
    )


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

    total_only = client.get(
        "/api/learning/study-time?include_days=false", headers=headers
    )
    assert total_only.status_code == 200
    assert total_only.json() == {"total_active_seconds": 1, "days": []}


def test_learning_sessions_accept_the_android_course_player(client):
    course_id = create_course(client, sign_in(client))
    headers = sign_in(client, "learner_test")

    started = client.post(
        "/api/learning/study-sessions",
        headers=headers,
        json={
            "course_id": course_id,
            "platform": "android",
            "entry_source": "course_player",
        },
    )

    assert started.status_code == 201
    assert started.json()["platform"] == "android"


def test_learning_sessions_accept_the_ipad_course_player(client):
    course_id = create_course(client, sign_in(client))
    headers = sign_in(client, "learner_test")

    started = client.post(
        "/api/learning/study-sessions",
        headers=headers,
        json={
            "course_id": course_id,
            "platform": "ios",
            "entry_source": "ipad_course_player",
        },
    )

    assert started.status_code == 201
    assert started.json()["platform"] == "ios"
