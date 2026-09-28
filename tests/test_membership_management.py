from datetime import datetime, timedelta

from tests.conftest import sign_in


def test_admin_configures_material_membership_and_course_access(client):
    admin_headers = sign_in(client)
    modules = client.get("/api/learning/modules").json()["items"]
    elementary = next(item for item in modules if item["module_code"] == "elementary-english")

    topic_response = client.post(
        "/api/admin/learning/topics",
        headers=admin_headers,
        json={
            "module_id": elementary["id"],
            "topic_code": "membership-dialogues",
            "title": "会员对话教材",
        },
    )
    assert topic_response.status_code == 201
    topic_id = topic_response.json()["id"]

    admin_topics = client.get("/api/admin/learning-topics", headers=admin_headers)
    assert admin_topics.status_code == 200
    assert any(topic["id"] == topic_id for topic in admin_topics.json()["items"])

    material_response = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": topic_id,
            "material_code": "talk-plus-1",
            "title": "Talk Plus 1",
            "material_type": "dialogue",
            "publisher": "Happy English",
        },
    )
    assert material_response.status_code == 201
    material_id = material_response.json()["id"]

    lesson_response = client.post(
        f"/api/admin/learning-materials/{material_id}/lessons",
        headers=admin_headers,
        json={
            "lesson_code": "unit-1",
            "title": "Unit 1: Hello",
            "source_resource": "textbook",
            "source_reference_id": 1,
            "estimated_minutes": 12,
        },
    )
    assert lesson_response.status_code == 201
    assert lesson_response.json()["source_resource"] == "textbook"

    # A private note cannot be published as a platform material lesson.
    private_note_lesson = client.post(
        f"/api/admin/learning-materials/{material_id}/lessons",
        headers=admin_headers,
        json={
            "lesson_code": "private-note",
            "title": "Private note",
            "source_resource": "notes",
            "source_reference_id": 1,
        },
    )
    assert private_note_lesson.status_code == 422

    course_response = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": topic_id,
            "material_id": material_id,
            "course_code": "talk-plus-1-course",
            "title": "Talk Plus 1 课程",
            "course_type": "dialogue",
            "access_policy": "benefit",
        },
    )
    assert course_response.status_code == 201
    course_id = course_response.json()["id"]

    admin_courses = client.get("/api/admin/learning-courses", headers=admin_headers)
    assert admin_courses.status_code == 200
    assert any(course["id"] == course_id for course in admin_courses.json()["items"])

    material_detail = client.get(f"/api/learning/materials/{material_id}")
    assert material_detail.status_code == 200
    assert [lesson["lesson_code"] for lesson in material_detail.json()["lessons"]] == ["unit-1"]
    assert "source_content" not in material_detail.json()["lessons"][0]

    plan_response = client.post(
        "/api/admin/membership-plans",
        headers=admin_headers,
        json={
            "plan_code": "talk-monthly",
            "name": "口语月卡",
            "billing_cycle": "monthly",
            "duration_days": 30,
            "price": "29.90",
            "status": "active",
            "is_default": True,
        },
    )
    assert plan_response.status_code == 201
    plan_id = plan_response.json()["id"]
    assert plan_response.json()["is_default"] == 1

    benefit_response = client.post(
        "/api/admin/membership-benefits",
        headers=admin_headers,
        json={
            "benefit_code": "talk-plus-access",
            "name": "Talk Plus 课程访问",
            "benefit_type": "content_access",
            "value_type": "boolean",
            "scope": {"module": "elementary-english"},
            "default_value": True,
        },
    )
    assert benefit_response.status_code == 201
    benefit_id = benefit_response.json()["id"]
    assert benefit_response.json()["default_value"] is True

    plan_benefits = client.put(
        f"/api/admin/membership-plans/{plan_id}/benefits",
        headers=admin_headers,
        json={"items": [{"benefit_id": benefit_id, "grant_value": True}]},
    )
    assert plan_benefits.status_code == 200
    assert plan_benefits.json()["items"][0]["grant_value"] is True

    benefit_courses = client.put(
        f"/api/admin/membership-benefits/{benefit_id}/courses",
        headers=admin_headers,
        json={"items": [{"course_id": course_id, "access_action": "study"}]},
    )
    assert benefit_courses.status_code == 200
    assert benefit_courses.json()["items"][0]["course_id"] == course_id

    learner_headers = sign_in(client, "learner_test")
    locked = client.post(
        "/api/learning/my-courses",
        headers=learner_headers,
        json={"course_id": course_id},
    )
    assert locked.status_code == 403

    # Member materials must not be retrievable through the old, resource-wide
    # content endpoint, which has no course context for applying the preview.
    assert client.get("/api/content/textbook", headers=learner_headers).status_code == 403
    assert client.get("/api/content/textbook/1", headers=learner_headers).status_code == 403

    starts_at = datetime.now().replace(microsecond=0)
    admin_headers = sign_in(client)
    grant = client.post(
        "/api/admin/users/2/memberships",
        headers=admin_headers,
        json={
            "membership_plan_id": plan_id,
            "status": "active",
            "source": "gift",
            "starts_at": starts_at.isoformat(),
            "ends_at": (starts_at + timedelta(days=30)).isoformat(),
        },
    )
    assert grant.status_code == 201
    assert grant.json()["membership_plan_id"] == plan_id

    learner_headers = sign_in(client, "learner_test")
    enrolled = client.post(
        "/api/learning/my-courses",
        headers=learner_headers,
        json={"course_id": course_id},
    )
    assert enrolled.status_code == 201
    assert enrolled.json()["access_state"] == "available"

    my_courses = client.get("/api/learning/my-courses", headers=learner_headers)
    assert my_courses.status_code == 200
    assert my_courses.json()["items"][0]["access_state"] == "available"
    assert my_courses.json()["items"][0]["material_title"] == "Talk Plus 1"

    opened = client.post(f"/api/learning/courses/{course_id}/open", headers=learner_headers)
    assert opened.status_code == 200
    assert opened.json()["material"]["id"] == material_id
    assert opened.json()["lessons"][0]["id"] == lesson_response.json()["id"]
    assert opened.json()["lessons"][0]["source_content"]["id"] == 1


def test_membership_configuration_requires_administrator(client):
    learner_headers = sign_in(client, "learner_test")

    forbidden = client.get("/api/admin/membership-plans", headers=learner_headers)

    assert forbidden.status_code == 403


def test_membership_course_previews_two_lessons_and_locks_the_rest(client):
    admin_headers = sign_in(client)
    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_code": "preview-material",
            "title": "会员试看教材",
            "material_type": "textbook",
        },
    )
    assert material.status_code == 201
    material_id = material.json()["id"]

    for number in range(1, 4):
        lesson = client.post(
            f"/api/admin/learning-materials/{material_id}/lessons",
            headers=admin_headers,
            json={
                "lesson_code": f"preview-{number}",
                "title": f"第 {number} 课",
                "content": {"blocks": [{"text": f"第 {number} 课正文"}]},
                "sort_order": number,
            },
        )
        assert lesson.status_code == 201

    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_id": material_id,
            "course_code": "preview-material-course",
            "title": "会员试看课程",
            "access_policy": "benefit",
        },
    )
    assert course.status_code == 201
    course_id = course.json()["id"]

    learner_headers = sign_in(client, "learner_test")
    preview = client.post(f"/api/learning/courses/{course_id}/open", headers=learner_headers)
    assert preview.status_code == 200
    preview_data = preview.json()
    assert preview_data["access_state"] == "preview"
    assert preview_data["preview_lesson_count"] == 2
    assert [lesson["is_locked"] for lesson in preview_data["lessons"]] == [
        False,
        False,
        True,
    ]
    assert "content" in preview_data["lessons"][0]
    assert "content" in preview_data["lessons"][1]
    assert "content" not in preview_data["lessons"][2]
    assert preview_data["lessons"][2]["lock_reason"] == "membership"

    material_preview = client.get(
        f"/api/learning/materials/{material_id}", headers=learner_headers
    )
    assert material_preview.status_code == 200
    material_preview_data = material_preview.json()
    assert material_preview_data["access_state"] == "preview"
    assert [lesson["is_locked"] for lesson in material_preview_data["lessons"]] == [
        False,
        False,
        True,
    ]
    locked_material_lesson = client.get(
        f"/api/learning/materials/{material_id}/lessons/{material_preview_data['lessons'][2]['id']}",
        headers=learner_headers,
    )
    assert locked_material_lesson.status_code == 403
    assert "需要会员解锁" in locked_material_lesson.json()["detail"]

    admin_headers = sign_in(client)
    plan = client.post(
        "/api/admin/membership-plans",
        headers=admin_headers,
        json={
            "plan_code": "preview-course-member",
            "name": "试看课程会员",
            "billing_cycle": "manual",
            "status": "active",
        },
    )
    benefit = client.post(
        "/api/admin/membership-benefits",
        headers=admin_headers,
        json={
            "benefit_code": "preview-course-access",
            "name": "试看课程访问权益",
            "benefit_type": "content_access",
            "value_type": "boolean",
        },
    )
    assert plan.status_code == 201
    assert benefit.status_code == 201
    assert (
        client.put(
            f"/api/admin/membership-plans/{plan.json()['id']}/benefits",
            headers=admin_headers,
            json={"items": [{"benefit_id": benefit.json()["id"]}]},
        ).status_code
        == 200
    )
    assert (
        client.put(
            f"/api/admin/membership-benefits/{benefit.json()['id']}/courses",
            headers=admin_headers,
            json={"items": [{"course_id": course_id, "access_action": "study"}]},
        ).status_code
        == 200
    )
    starts_at = datetime.now().replace(microsecond=0)
    grant = client.post(
        "/api/admin/users/2/memberships",
        headers=admin_headers,
        json={
            "membership_plan_id": plan.json()["id"],
            "status": "active",
            "source": "gift",
            "starts_at": starts_at.isoformat(),
            "ends_at": (starts_at + timedelta(days=30)).isoformat(),
        },
    )
    assert grant.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    unlocked = client.post(f"/api/learning/courses/{course_id}/open", headers=learner_headers)
    assert unlocked.status_code == 200
    unlocked_data = unlocked.json()
    assert unlocked_data["access_state"] == "available"
    assert [lesson["is_locked"] for lesson in unlocked_data["lessons"]] == [
        False,
        False,
        False,
    ]
    assert "content" in unlocked_data["lessons"][2]

    material_unlocked = client.get(
        f"/api/learning/materials/{material_id}", headers=learner_headers
    )
    assert material_unlocked.json()["access_state"] == "available"
    assert all(not lesson["is_locked"] for lesson in material_unlocked.json()["lessons"])


def test_membership_preview_counts_lessons_across_linked_materials(client):
    admin_headers = sign_in(client)
    materials = []
    lessons = []
    for material_code, title, lesson_count in [
        ("preview-multi-one", "试看教材一", 1),
        ("preview-multi-two", "试看教材二", 2),
    ]:
        material = client.post(
            "/api/admin/learning-materials",
            headers=admin_headers,
            json={
                "topic_id": 2,
                "material_code": material_code,
                "title": title,
                "material_type": "textbook",
            },
        )
        assert material.status_code == 201
        materials.append(material.json())
        for number in range(lesson_count):
            lesson = client.post(
                f"/api/admin/learning-materials/{material.json()['id']}/lessons",
                headers=admin_headers,
                json={
                    "lesson_code": f"{material_code}-{number + 1}",
                    "title": f"{title}第 {number + 1} 课",
                    "content": {"blocks": [{"text": title}]},
                    "sort_order": number + 1,
                },
            )
            assert lesson.status_code == 201
            lessons.append(lesson.json())

    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_ids": [material["id"] for material in materials],
            "course_code": "preview-multi-material-course",
            "title": "跨教材试看课程",
            "access_policy": "benefit",
        },
    )
    assert course.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    preview = client.post(
        f"/api/learning/courses/{course.json()['id']}/open", headers=learner_headers
    )
    assert preview.status_code == 200
    data = preview.json()
    assert data["access_state"] == "preview"
    assert [lesson["id"] for lesson in data["lessons"]] == [lesson["id"] for lesson in lessons]
    assert [lesson["is_locked"] for lesson in data["lessons"]] == [False, False, True]
    assert [lesson["is_locked"] for lesson in data["materials"][1]["lessons"]] == [False, True]


def test_new_registration_receives_the_configured_default_membership(client):
    admin_headers = sign_in(client)
    plan = client.post(
        "/api/admin/membership-plans",
        headers=admin_headers,
        json={
            "plan_code": "starter-free",
            "name": "新手会员",
            "billing_cycle": "free",
            "status": "active",
            "is_default": True,
        },
    )
    assert plan.status_code == 201

    signup = client.post(
        "/api/auth/signup",
        headers=admin_headers,
        json={
            "username": "new_learner",
            "password": "Testing123!",
            "full_name": "新同学",
            "email": "new_learner@example.com",
        },
    )
    assert signup.status_code == 201

    memberships = client.get(
        f"/api/admin/users/{signup.json()['id']}/memberships",
        headers=admin_headers,
    )
    assert memberships.status_code == 200
    assert memberships.json()["items"][0]["membership_plan_id"] == plan.json()["id"]
    assert memberships.json()["items"][0]["source"] == "signup"


def test_cannot_issue_an_inactive_membership_plan(client):
    admin_headers = sign_in(client)
    plan = client.post(
        "/api/admin/membership-plans",
        headers=admin_headers,
        json={
            "plan_code": "inactive-plan",
            "name": "未启用会员等级",
            "billing_cycle": "manual",
            "status": "inactive",
        },
    )
    assert plan.status_code == 201

    response = client.post(
        "/api/admin/users/2/memberships",
        headers=admin_headers,
        json={
            "membership_plan_id": plan.json()["id"],
            "status": "active",
            "source": "manual",
            "starts_at": datetime.now().replace(microsecond=0).isoformat(),
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "只能发放已启用的会员等级，请先在“会员等级”中将该等级设为启用。"


def test_membership_admin_lists_filter_and_paginate(client):
    admin_headers = sign_in(client)
    created_plans = []
    for suffix in ("one", "two"):
        response = client.post(
            "/api/admin/membership-plans",
            headers=admin_headers,
            json={
                "plan_code": f"paged-plan-{suffix}",
                "name": f"分页会员 {suffix}",
                "billing_cycle": "manual",
                "status": "active",
            },
        )
        assert response.status_code == 201
        created_plans.append(response.json())

    plans = client.get(
        "/api/admin/membership-plans?q=%E5%88%86%E9%A1%B5%E4%BC%9A%E5%91%98&page=1&page_size=1",
        headers=admin_headers,
    )
    assert plans.status_code == 200
    assert plans.json()["total"] == 2
    assert plans.json()["total_pages"] == 2
    assert len(plans.json()["items"]) == 1

    benefit = client.post(
        "/api/admin/membership-benefits",
        headers=admin_headers,
        json={
            "benefit_code": "paged-feature",
            "name": "分页功能权益",
            "benefit_type": "feature_access",
            "value_type": "boolean",
        },
    )
    assert benefit.status_code == 201
    benefits = client.get(
        "/api/admin/membership-benefits?benefit_type=feature_access&page_size=1",
        headers=admin_headers,
    )
    assert benefits.status_code == 200
    assert benefits.json()["total"] == 1
    assert benefits.json()["items"][0]["id"] == benefit.json()["id"]

    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": 1,
            "material_code": "paged-material",
            "title": "分页教材",
            "material_type": "textbook",
        },
    )
    assert material.status_code == 201
    materials = client.get(
        "/api/admin/learning-materials?q=%E5%88%86%E9%A1%B5%E6%95%99%E6%9D%90&page_size=1",
        headers=admin_headers,
    )
    assert materials.status_code == 200
    assert materials.json()["total"] == 1

    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 1,
            "material_id": material.json()["id"],
            "course_code": "paged-material-course",
            "title": "分页教材课程",
        },
    )
    assert course.status_code == 201
    courses = client.get(
        f"/api/admin/learning-courses?material_id={material.json()['id']}&page_size=1",
        headers=admin_headers,
    )
    assert courses.status_code == 200
    assert courses.json()["total"] == 1
    assert courses.json()["items"][0]["id"] == course.json()["id"]

    starts_at = datetime.now().replace(microsecond=0)
    issued = client.post(
        "/api/admin/users/2/memberships",
        headers=admin_headers,
        json={
            "membership_plan_id": created_plans[0]["id"],
            "status": "active",
            "source": "manual",
            "starts_at": starts_at.isoformat(),
            "ends_at": (starts_at + timedelta(days=7)).isoformat(),
        },
    )
    assert issued.status_code == 201
    memberships = client.get(
        f"/api/admin/user-memberships?q=learner_test&membership_plan_id={created_plans[0]['id']}",
        headers=admin_headers,
    )
    assert memberships.status_code == 200
    assert memberships.json()["total"] == 1
    assert memberships.json()["items"][0]["user_id"] == 2
