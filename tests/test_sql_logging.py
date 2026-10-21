from tests.conftest import sign_in


def test_sql_logging_records_statements_conditions_and_transactions(client):
    sign_in(client, "learner_test")
    response = client.get("/api/learning/modules")
    assert response.status_code == 200

    log_text = client.app.state.settings.log_file.read_text()
    assert "sql.query" in log_text
    assert "SELECT" in log_text
    assert "params=" in log_text
    assert "duration_ms=" in log_text
    assert "sql.transaction action=commit" in log_text or "sql.transaction action=rollback" in log_text
