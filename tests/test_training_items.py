from tests.conftest import opaque_id, sign_in


def test_training_items_support_podcast_metadata_and_opaque_ids(client):
    headers = sign_in(client)
    module = client.post(
        "/api/admin/learning/modules",
        headers=headers,
        json={
            "module_code": "podcast-training-test",
            "module_type": "training",
            "name": "Podcast 训练",
            "name_en": "Podcast Training",
            "route_key": "podcast-training-test",
            "sort_order": 90,
        },
    )
    assert module.status_code == 201
    module_id = module.json()["id"]

    created = client.post(
        "/api/admin/learning-training-items",
        headers=headers,
        json={
            "module_id": module_id,
            "resource_type": "podcast",
            "item_code": "daily-life-test",
            "title": "生活场景听力",
            "title_en": "Daily Life Listening",
            "summary": "练习听懂真实语速。",
            "description": "一节完整的生活场景听力训练。",
            "cover_image_url": "/static/training/podcast/daily-life-test.jpg",
            "audio_url": "/static/training/podcast/daily-life-test.mp3",
            "subtitle_url": "/static/training/podcast/daily-life-test.vtt",
            "difficulty_code": "A2",
            "duration_seconds": 754,
            "episode_number": 1,
            "speaker": "HappyLingo Podcast",
            "sort_order": 10,
        },
    )
    assert created.status_code == 201
    item = created.json()
    assert item["id"].startswith("hei1_")
    assert item["module_id"] == module_id
    assert item["audio_url"].endswith(".mp3")
    assert item["subtitle_url"].endswith(".vtt")

    listing = client.get(
        f"/api/learning/app/training-items?module_id={module_id}&resource_type=podcast",
        headers=headers,
    )
    assert listing.status_code == 200
    assert [entry["id"] for entry in listing.json()["items"]] == [item["id"]]
    assert listing.json()["items"][0]["difficulty_code"] == "A2"

    detail = client.get(f"/api/learning/app/training-items/{item['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == item["id"]

    admin_list = client.get(
        "/api/admin/learning-training-items?resource_type=podcast",
        headers=headers,
    )
    assert admin_list.status_code == 200
    assert any(entry["id"] == item["id"] for entry in admin_list.json()["items"])

    assert client.get("/api/learning/app/training-items?module_id=1", headers=headers).status_code == 422
    assert client.post(
        "/api/admin/learning-training-items",
        headers=headers,
        json={
            "module_id": 1,
            "item_code": "raw-module-id",
            "title": "必须使用加密 ID",
        },
    ).status_code == 422


def test_training_item_requires_a_training_module(client):
    headers = sign_in(client)
    response = client.post(
        "/api/admin/learning-training-items",
        headers=headers,
        json={
            "module_id": opaque_id(client, 2),
            "item_code": "wrong-module",
            "title": "错误模块",
        },
    )
    assert response.status_code == 422
