from tests.conftest import sign_in


def test_request_logging_includes_inputs_and_outputs_without_credentials(client):
    assert client.get("/api/health").status_code == 200
    csrf = client.get("/api/auth/session?token=should-not-be-logged").json()["csrf_token"]
    response = client.post(
        "/api/auth/login",
        json={"username": "admin_test", "password": "Testing123!"},
        headers={"X-CSRF-Token": csrf},
    )
    assert response.status_code == 200

    log_text = client.app.state.settings.log_file.read_text()
    assert "http.request.input" in log_text
    assert "http.request.output" in log_text
    assert '"status":"ok"' in log_text
    assert "admin_test" in log_text
    assert "[REDACTED]" in log_text
    assert "Testing123!" not in log_text
    assert "should-not-be-logged" not in log_text


def test_request_logging_describes_binary_response_without_dumping_audio(client):
    sign_in(client, "learner_test")
    response = client.get("/static/training/podcast/unknown.mp3")
    assert response.status_code == 404
    log_text = client.app.state.settings.log_file.read_text()
    assert "http.request.output" in log_text
