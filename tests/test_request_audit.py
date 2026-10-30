from tests.conftest import sign_in


def test_admin_can_query_user_request_activity_from_application_logs(client):
    headers = sign_in(client)

    listed = client.get("/api/admin/users", headers=headers)
    assert listed.status_code == 200

    response = client.get(
        "/api/admin/request-audits?username=admin_test&path=%2Fapi%2Fadmin%2Fusers&method=GET",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["username"] == "admin_test"
    assert data["items"][0]["path"] == "/api/admin/users"
    assert data["items"][0]["method"] == "GET"
    assert data["items"][0]["status"] == 200

    report = client.get(
        "/api/admin/request-audits/report?username=admin_test&path=%2Fapi%2Fadmin%2Fusers",
        headers=headers,
    )
    assert report.status_code == 200
    payload = report.json()
    assert payload["overview"]["requests"] >= 1
    assert payload["overview"]["p90_ms"] is not None
    assert "active_users_today" in payload["overview"]
    assert "active_users_today_date" in payload["overview"]
    assert "active_users_today_list" in payload["overview"]
    assert payload["users"][0]["username"] == "admin_test"
    assert payload["endpoints"][0]["path"] == "/api/admin/users"
    assert payload["daily"]
    assert "active_users" in payload["daily"][0]

    user_report = client.get(
        "/api/admin/request-audits/user-report?path=%2Fapi%2Fadmin%2Fusers",
        headers=headers,
    )
    assert user_report.status_code == 200
    assert all(item["username"] != "游客" for item in user_report.json()["users"])

    latency_report = client.get(
        "/api/admin/request-audits/latency-report?path=%2Fapi%2Fadmin%2Fusers",
        headers=headers,
    )
    assert latency_report.status_code == 200
    assert latency_report.json()["endpoints"][0]["p99_ms"] is not None
