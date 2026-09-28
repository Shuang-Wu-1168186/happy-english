from tests.conftest import sign_in


def test_learning_catalog_shows_the_six_english_levels_and_only_ready_topics(client):
    sign_in(client, "learner_test")

    response = client.get("/api/learning/modules")

    assert response.status_code == 200
    assert [item["module_code"] for item in response.json()["items"]] == [
        "beginner-english",
        "elementary-english",
        "intermediate-english",
        "advanced-english",
        "higher-english",
        "private-zone",
    ]
    assert [item["name"] for item in response.json()["items"]] == [
        "入门英语",
        "初级英语",
        "中级英语",
        "进阶英语",
        "高级英语",
        "私人专区",
    ]

    beginner = next(item for item in response.json()["items"] if item["module_code"] == "beginner-english")
    detail = client.get(f"/api/learning/modules/{beginner['id']}")
    assert detail.status_code == 200
    assert [topic["topic_code"] for topic in detail.json()["topics"]] == ["natural-phonics"]

    elementary = next(
        item for item in response.json()["items"] if item["module_code"] == "elementary-english"
    )
    detail = client.get(f"/api/learning/modules/{elementary['id']}")
    assert detail.status_code == 200
    assert [topic["topic_code"] for topic in detail.json()["topics"]] == ["daily-speaking-dialogues"]

    for module in response.json()["items"][2:5]:
        detail = client.get(f"/api/learning/modules/{module['id']}")
        assert detail.status_code == 200
        assert detail.json()["topics"] == []

    private_zone = next(
        item for item in response.json()["items"] if item["module_code"] == "private-zone"
    )
    detail = client.get(f"/api/learning/modules/{private_zone['id']}")
    assert detail.status_code == 200
    assert [topic["topic_code"] for topic in detail.json()["topics"]] == [
        "my-english-notes"
    ]


def test_learning_catalog_admin_builds_a_topic_and_course_hierarchy(client):
    headers = sign_in(client)
    modules = client.get("/api/learning/modules").json()["items"]
    elementary = next(item for item in modules if item["module_code"] == "elementary-english")

    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": elementary["id"],
            "topic_code": "at-the-restaurant",
            "title": "餐厅英语",
            "title_en": "At the Restaurant",
            "description": "点餐、确认菜品和结账。",
            "sort_order": 10,
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]
    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "course_code": "ordering-food-01",
            "title": "点餐",
            "course_type": "dialogue",
            "content_resource": "dialogues",
            "estimated_minutes": 8,
            "content": {
                "blocks": [
                    {
                        "type": "dialogue",
                        "speaker": "Customer",
                        "english": "I'd like the soup, please.",
                        "chinese": "我想要这份汤。",
                    }
                ]
            },
        },
    )
    assert course.status_code == 201
    course_id = course.json()["id"]
    assert course.json()["content"]["blocks"][0]["speaker"] == "Customer"

    sign_in(client, "learner_test")
    module_detail = client.get(f"/api/learning/modules/{elementary['id']}")
    assert module_detail.status_code == 200
    assert any(topic["id"] == topic_id for topic in module_detail.json()["topics"])

    topic_detail = client.get(f"/api/learning/topics/{topic_id}")
    assert topic_detail.status_code == 200
    assert topic_detail.json()["courses"][0]["id"] == course_id

    course_detail = client.get(f"/api/learning/courses/{course_id}")
    assert course_detail.status_code == 200
    assert course_detail.json()["content"]["blocks"][0]["english"] == "I'd like the soup, please."


def test_top_level_course_catalog_omits_hidden_topics(client):
    headers = sign_in(client)
    public_course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": 2,
            "course_code": "phonics-visible-course",
            "title": "自然拼读公开课程",
        },
    )
    assert public_course.status_code == 201
    hidden_course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": 1,
            "course_code": "textbook-hidden-course",
            "title": "暂不展示的课本课程",
        },
    )
    assert hidden_course.status_code == 201

    sign_in(client, "learner_test")
    response = client.get("/api/learning/courses")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()["items"]] == [public_course.json()["id"]]
    assert client.get("/api/learning/courses?topic_id=1").status_code == 404


def test_admin_can_maintain_topics_with_statistics_and_publication(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "topic-maintenance",
            "title": "专题维护测试",
            "description": "用于验证专题后台维护。",
            "sort_order": 90,
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]

    material = client.post(
        "/api/admin/learning-materials",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_code": "topic-maintenance-material",
            "title": "专题教材",
            "material_type": "textbook",
        },
    )
    assert material.status_code == 201
    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_id": material.json()["id"],
            "course_code": "topic-maintenance-course",
            "title": "专题课程",
        },
    )
    assert course.status_code == 201

    listing = client.get(
        "/api/admin/learning-topics?q=维护&page=1&page_size=10", headers=headers
    )
    assert listing.status_code == 200
    managed = next(item for item in listing.json()["items"] if item["id"] == topic_id)
    assert listing.json()["total"] == 1
    assert managed["statistics"] == {
        "material_count": 1,
        "published_material_count": 1,
        "lesson_count": 0,
        "published_lesson_count": 0,
        "course_count": 1,
        "published_course_count": 1,
    }

    detail = client.get(f"/api/admin/learning-topics/{topic_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["materials"][0]["id"] == material.json()["id"]
    assert detail.json()["courses"][0]["id"] == course.json()["id"]

    unpublished = client.put(
        f"/api/admin/learning/topics/{topic_id}/publication",
        headers=headers,
        json={"is_published": 0},
    )
    assert unpublished.status_code == 200
    assert unpublished.json()["is_published"] == 0
    assert client.get(f"/api/learning/topics/{topic_id}").status_code == 404
    assert client.delete(f"/api/admin/learning/topics/{topic_id}", headers=headers).status_code == 409


def test_admin_can_order_courses_within_a_topic_and_learners_receive_that_order(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "ordered-topic",
            "title": "课程排序测试",
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]

    course_ids = []
    for code, title, sort_order in [
        ("ordered-first", "第一节", 30),
        ("ordered-second", "第二节", 10),
        ("ordered-third", "第三节", 20),
    ]:
        course = client.post(
            "/api/admin/learning/courses",
            headers=headers,
            json={
                "topic_id": topic_id,
                "course_code": code,
                "title": title,
                "sort_order": sort_order,
            },
        )
        assert course.status_code == 201
        course_ids.append(course.json()["id"])

    order = [course_ids[2], course_ids[0], course_ids[1]]
    reordered = client.put(
        f"/api/admin/learning-topics/{topic_id}/course-order",
        headers=headers,
        json={"course_ids": order},
    )
    assert reordered.status_code == 200
    assert [item["id"] for item in reordered.json()["items"]] == order
    assert [item["sort_order"] for item in reordered.json()["items"]] == [10, 20, 30]

    invalid = client.put(
        f"/api/admin/learning-topics/{topic_id}/course-order",
        headers=headers,
        json={"course_ids": [course_ids[0], course_ids[0], course_ids[1]]},
    )
    assert invalid.status_code == 422

    sign_in(client, "learner_test")
    topic_detail = client.get(f"/api/learning/topics/{topic_id}")
    assert topic_detail.status_code == 200
    assert [course["id"] for course in topic_detail.json()["courses"]] == order
    course_listing = client.get(f"/api/learning/courses?topic_id={topic_id}")
    assert course_listing.status_code == 200
    assert [course["id"] for course in course_listing.json()["items"]] == order


def test_admin_can_associate_existing_courses_with_a_topic(client):
    headers = sign_in(client)
    target = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "course-association-target",
            "title": "课程关联目标",
        },
    )
    source = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "course_code": "course-association-source",
            "title": "待关联课程",
        },
    )
    assert target.status_code == 201
    assert source.status_code == 201
    target_id = target.json()["id"]
    course_id = source.json()["id"]

    associated = client.post(
        f"/api/admin/learning-topics/{target_id}/courses",
        headers=headers,
        json={"course_ids": [course_id]},
    )
    assert associated.status_code == 200
    assert [item["id"] for item in associated.json()["items"]] == [course_id]
    assert associated.json()["items"][0]["topic_ids"] == [target_id]

    second_target = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "course-association-second-target",
            "title": "课程关联第二专题",
        },
    )
    assert second_target.status_code == 201
    second_target_id = second_target.json()["id"]
    second_association = client.post(
        f"/api/admin/learning-topics/{second_target_id}/courses",
        headers=headers,
        json={"course_ids": [course_id]},
    )
    assert second_association.status_code == 200
    assert set(second_association.json()["items"][0]["topic_ids"]) == {
        target_id,
        second_target_id,
    }
    removed = client.delete(
        f"/api/admin/learning-topics/{target_id}/courses/{course_id}",
        headers=headers,
    )
    assert removed.status_code == 204
    course_listing = client.get(
        f"/api/admin/learning-courses?topic_id={second_target_id}",
        headers=headers,
    )
    assert course_listing.status_code == 200
    assert [course["id"] for course in course_listing.json()["items"]] == [course_id]


def test_admin_can_remove_an_unreferenced_course_and_keep_its_material(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "removable-course-topic",
            "title": "可移除课程专题",
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]
    material = client.post(
        "/api/admin/learning-materials",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_code": "removable-course-material",
            "title": "保留教材",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201
    material_id = material.json()["id"]
    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_ids": [material_id],
            "course_code": "removable-course",
            "title": "可移除课程",
        },
    )
    assert course.status_code == 201

    removed = client.delete(
        f"/api/admin/learning/courses/{course.json()['id']}", headers=headers
    )
    assert removed.status_code == 204

    material_detail = client.get(
        f"/api/admin/learning-materials/{material_id}", headers=headers
    )
    assert material_detail.status_code == 200
    assert material_detail.json()["courses"] == []
    topic_detail = client.get(f"/api/admin/learning-topics/{topic_id}", headers=headers)
    assert topic_detail.status_code == 200
    assert topic_detail.json()["courses"] == []


def test_admin_cannot_remove_a_course_with_learner_records(client):
    admin_headers = sign_in(client)
    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "course_code": "course-with-learner-record",
            "title": "已有学习记录的课程",
        },
    )
    assert course.status_code == 201
    course_id = course.json()["id"]

    learner_headers = sign_in(client, "learner_test")
    enrolled = client.post(
        "/api/learning/my-courses",
        headers=learner_headers,
        json={"course_id": course_id},
    )
    assert enrolled.status_code == 201

    admin_headers = sign_in(client)
    removed = client.delete(f"/api/admin/learning/courses/{course_id}", headers=admin_headers)
    assert removed.status_code == 409
    assert "用户课程" in removed.json()["detail"]


def test_admin_topic_order_returns_linked_material_labels(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "linked-material-order-label",
            "title": "教材名称排序测试",
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]

    material = client.post(
        "/api/admin/learning-materials",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_code": "linked-material-label",
            "title": "教材当前名称",
            "title_en": "Current Material Label",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201

    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_id": material.json()["id"],
            "course_code": "old-course-label",
            "title": "旧课程名称",
            "title_en": "Old Course Label",
        },
    )
    assert course.status_code == 201

    detail = client.get(f"/api/admin/learning-topics/{topic_id}")
    assert detail.status_code == 200
    ordered_course = detail.json()["courses"][0]
    assert ordered_course["title"] == "旧课程名称"
    assert ordered_course["material_title"] == "教材当前名称"
    assert ordered_course["material_title_en"] == "Current Material Label"
    assert ordered_course["material_code"] == "linked-material-label"


def test_renaming_a_material_updates_an_inherited_linked_course_name(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={"module_id": 2, "topic_code": "material-course-title", "title": "教材课程标题"},
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]
    material = client.post(
        "/api/admin/learning-materials",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_code": "inherited-course-material",
            "title": "原教材名称",
            "title_en": "Original Material",
            "material_type": "textbook",
        },
    )
    assert material.status_code == 201
    inherited = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_id": material.json()["id"],
            "course_code": "inherited-course",
            "title": "原教材名称",
            "title_en": "Original Material",
        },
    )
    custom = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_id": material.json()["id"],
            "course_code": "custom-course",
            "title": "自定义课程名称",
            "title_en": "Custom Course",
        },
    )
    assert inherited.status_code == 201
    assert custom.status_code == 201

    renamed = client.put(
        f"/api/admin/learning-materials/{material.json()['id']}",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_code": "inherited-course-material",
            "title": "新教材名称",
            "title_en": "Renamed Material",
            "material_type": "textbook",
        },
    )
    assert renamed.status_code == 200
    courses = client.get(
        f"/api/admin/learning-courses?material_id={material.json()['id']}&page_size=10",
        headers=headers,
    )
    assert courses.status_code == 200
    by_id = {course["id"]: course for course in courses.json()["items"]}
    assert by_id[inherited.json()["id"]]["title"] == "新教材名称"
    assert by_id[inherited.json()["id"]]["title_en"] == "Renamed Material"
    assert by_id[custom.json()["id"]]["title"] == "自定义课程名称"
    assert by_id[custom.json()["id"]]["title_en"] == "Custom Course"


def test_course_can_link_multiple_materials_and_preserves_their_lesson_order(client):
    headers = sign_in(client)
    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "multi-material-course",
            "title": "多教材课程",
        },
    )
    assert topic.status_code == 201
    topic_id = topic.json()["id"]
    other_topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "multi-material-linked-topic",
            "title": "可关联教材专题",
        },
    )
    assert other_topic.status_code == 201

    materials = []
    lessons = []
    for code, title, material_topic_id in [
        ("multi-material-first", "第一本教材", topic_id),
        ("multi-material-second", "第二本教材", other_topic.json()["id"]),
    ]:
        material = client.post(
            "/api/admin/learning-materials",
            headers=headers,
            json={
                "topic_id": material_topic_id,
                "material_code": code,
                "title": title,
                "material_type": "textbook",
            },
        )
        assert material.status_code == 201
        materials.append(material.json())
        lesson = client.post(
            f"/api/admin/learning-materials/{material.json()['id']}/lessons",
            headers=headers,
            json={
                "lesson_code": f"{code}-lesson",
                "title": f"{title}课时",
                "content": {"blocks": [{"text": title}]},
            },
        )
        assert lesson.status_code == 201
        lessons.append(lesson.json())

    course = client.post(
        "/api/admin/learning/courses",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_ids": [materials[1]["id"], materials[0]["id"]],
            "course_code": "multi-material-course",
            "title": "两本教材组成的课程",
        },
    )
    assert course.status_code == 201
    course_data = course.json()
    course_id = course_data["id"]
    assert course_data["material_ids"] == [materials[1]["id"], materials[0]["id"]]
    assert [item["id"] for item in course_data["materials"]] == course_data["material_ids"]
    # Existing clients still receive the first linked material in material_id.
    assert course_data["material_id"] == materials[1]["id"]

    for material in materials:
        filtered = client.get(
            f"/api/admin/learning-courses?material_id={material['id']}",
            headers=headers,
        )
        assert filtered.status_code == 200
        assert [item["id"] for item in filtered.json()["items"]] == [course_id]
        detail = client.get(
            f"/api/admin/learning-materials/{material['id']}", headers=headers
        )
        assert [item["id"] for item in detail.json()["courses"]] == [course_id]

    learner_headers = sign_in(client, "learner_test")
    opened = client.post(
        f"/api/learning/courses/{course_id}/open", headers=learner_headers
    )
    assert opened.status_code == 200
    opened_data = opened.json()
    assert [item["id"] for item in opened_data["materials"]] == [
        materials[1]["id"],
        materials[0]["id"],
    ]
    assert [item["id"] for item in opened_data["lessons"]] == [
        lessons[1]["id"],
        lessons[0]["id"],
    ]
    assert [item["id"] for item in opened_data["materials"][0]["lessons"]] == [
        lessons[1]["id"]
    ]

    headers = sign_in(client)
    updated = client.put(
        f"/api/admin/learning/courses/{course_id}",
        headers=headers,
        json={
            "topic_id": topic_id,
            "material_ids": [materials[0]["id"]],
            "course_code": "multi-material-course",
            "title": "两本教材组成的课程",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["material_ids"] == [materials[0]["id"]]
    removed_filter = client.get(
        f"/api/admin/learning-courses?material_id={materials[1]['id']}", headers=headers
    )
    assert removed_filter.json()["items"] == []


def test_admin_management_menu_includes_content_development_pages(client):
    headers = sign_in(client)

    response = client.get("/api/admin/management-menu", headers=headers)

    assert response.status_code == 200
    assert response.json()["items"] == [
        {
            "code": "learning-content",
            "title": "学习内容管理",
            "icon": "book-open",
            "children": [
                {
                    "code": "topic-maintenance",
                    "title": "专题维护",
                    "path": "/admin/content/topics",
                    "description": "维护专题、专题内课程管理、封面和发布状态。",
                },
                {
                    "code": "material-maintenance",
                    "title": "教材开发",
                    "path": "/admin/learning/materials",
                    "description": "开发教材并编排教材内的多个课时。",
                },
                {
                    "code": "template-maintenance",
                    "title": "模板管理",
                    "path": "/admin/content/templates",
                    "description": "维护 Web 和小程序共用的教材渲染模板。",
                },
                {
                    "code": "course-maintenance",
                    "title": "课程开发",
                    "path": "/admin/learning/courses",
                    "description": "组合多个教材，并设置免费或会员权益课程。",
                },
            ],
        }
    ]

    sign_in(client, "learner_test")
    assert client.get("/api/admin/management-menu").status_code == 403


def test_material_template_is_a_versioned_cross_client_renderer_contract(client):
    headers = sign_in(client)
    created_template = client.post(
        "/api/admin/learning-templates",
        headers=headers,
        json={
            "template_code": "standard",
            "template_version": 1,
            "name": "通用课时",
            "description": "测试模板",
            "content_kind": "source",
            "supported_clients": ["web", "mini"],
            "config": {"accent": "indigo"},
            "status": "active",
            "sort_order": 10,
        },
    )
    assert created_template.status_code == 201
    assert created_template.json()["renderer"] == "standard.v1"
    assert created_template.json()["supported_clients"] == ["web", "mini"]

    unsupported = client.post(
        "/api/admin/learning-templates",
        headers=headers,
        json={
            "template_code": "unknown-client-page",
            "template_version": 1,
            "name": "不存在的客户端页",
            "content_kind": "source",
            "supported_clients": ["web", "mini"],
        },
    )
    assert unsupported.status_code == 422

    topic = client.post(
        "/api/admin/learning/topics",
        headers=headers,
        json={
            "module_id": 2,
            "topic_code": "template-contract-topic",
            "title": "模板契约专题",
        },
    )
    assert topic.status_code == 201
    material = client.post(
        "/api/admin/learning-materials",
        headers=headers,
        json={
            "topic_id": topic.json()["id"],
            "template_id": created_template.json()["id"],
            "material_code": "template-contract-material",
            "title": "模板契约教材",
            "material_type": "note_collection",
        },
    )
    assert material.status_code == 201
    assert material.json()["template"]["renderer"] == "standard.v1"

    lesson = client.post(
        f"/api/admin/learning-materials/{material.json()['id']}/lessons",
        headers=headers,
        json={
            "lesson_code": "template-contract-lesson",
            "title": "模板课时",
            "content": {
                "items": [
                    {
                        "title": "Hello",
                        "english": "Hello, template.",
                        "chinese": "你好，模板。",
                    }
                ]
            },
        },
    )
    assert lesson.status_code == 201

    sign_in(client, "learner_test")
    detail = client.get(
        f"/api/learning/materials/{material.json()['id']}/lessons/{lesson.json()['id']}"
    )
    assert detail.status_code == 200
    assert detail.json()["template"]["renderer"] == "standard.v1"
    assert detail.json()["render_payload"] == {
        "template": detail.json()["template"],
        "content_kind": "source",
        "source_resource": None,
        "content": {
            "items": [
                {
                    "title": "Hello",
                    "english": "Hello, template.",
                    "chinese": "你好，模板。",
                }
            ]
        },
    }
