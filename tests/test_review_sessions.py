import json
from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy import select

from app import models as m
from app.core.config import Settings
from app.main import _redact_review_request
from app.services.review_ai import (
    DeepSeekReviewQuestionGenerator,
    ReviewCandidate,
    ReviewQuestionPlan,
    ReviewSelection,
)
from tests.conftest import opaque_id, sign_in


def seed_note_progress(client):
    with client.app.state.engine.begin() as connection:
        connection.execute(
            m.english_note_item.update()
            .where(m.english_note_item.c.id == 1)
            .values(
                examples="Could you wait for me?\n你能等我一下吗？",
                explanation="用于请对方稍等。",
            )
        )
    headers = sign_in(client, "learner_test")
    saved = client.post(
        "/api/progress",
        headers=headers,
        json={
            "content_type": "english_note",
            "parent_id": opaque_id(client, 1),
            "item_id": opaque_id(client, 1),
        },
    )
    assert saved.status_code == 200
    return headers


def grant_ai_review_generation(client, username="learner_test"):
    """Give one fixture learner the explicit AI-review feature entitlement."""

    now = datetime.now(UTC).replace(tzinfo=None)
    with client.app.state.engine.begin() as connection:
        user_id = connection.scalar(
            select(m.user.c.id).where(m.user.c.username == username)
        )
        plan_id = connection.execute(
            m.membership_plan.insert().values(
                plan_code="review-ai-test",
                name="AI 复习测试会员",
                billing_cycle="manual",
                price=0,
                currency="CNY",
                status="active",
            )
        ).inserted_primary_key[0]
        benefit_id = connection.execute(
            m.membership_benefit.insert().values(
                benefit_code="ai-review-generation",
                name="AI 智能复习出题",
                benefit_type="feature_access",
                value_type="boolean",
                default_value_json="true",
                status="active",
            )
        ).inserted_primary_key[0]
        connection.execute(
            m.membership_plan_benefit.insert().values(
                membership_plan_id=plan_id,
                benefit_id=benefit_id,
                grant_value_json="true",
                is_enabled=1,
            )
        )
        connection.execute(
            m.user_membership.insert().values(
                user_id=user_id,
                membership_plan_id=plan_id,
                status="active",
                source="manual",
                starts_at=now - timedelta(minutes=1),
                ends_at=now + timedelta(days=1),
            )
        )


def grant_membership_without_ai_review_generation(client, username="learner_test"):
    """A paid membership alone must not enable a separately scoped feature."""

    now = datetime.now(UTC).replace(tzinfo=None)
    with client.app.state.engine.begin() as connection:
        user_id = connection.scalar(
            select(m.user.c.id).where(m.user.c.username == username)
        )
        plan_id = connection.execute(
            m.membership_plan.insert().values(
                plan_code="review-no-ai-test",
                name="基础测试会员",
                billing_cycle="manual",
                price=0,
                currency="CNY",
                status="active",
            )
        ).inserted_primary_key[0]
        connection.execute(
            m.user_membership.insert().values(
                user_id=user_id,
                membership_plan_id=plan_id,
                status="active",
                source="manual",
                starts_at=now - timedelta(minutes=1),
                ends_at=now + timedelta(days=1),
            )
        )


def test_review_session_filters_notes_and_textbooks(client):
    headers = seed_note_progress(client)

    notes = client.post(
        "/api/learning/review-sessions",
        headers=headers,
        json={"days": 7, "limit": 10, "source_types": ["notes"]},
    )
    assert notes.status_code == 201
    assert notes.json()["source_types"] == ["notes"]
    assert notes.json()["generation"]["fallback"] is True
    assert notes.json()["questions"]
    assert all(
        question["source"]["type"] == "english_note_item"
        for question in notes.json()["questions"]
    )

    textbooks = client.post(
        "/api/learning/review-sessions",
        headers=headers,
        json={"days": 7, "limit": 10, "source_types": ["textbooks"]},
    )
    assert textbooks.status_code == 201
    assert textbooks.json()["source_types"] == ["textbooks"]
    assert textbooks.json()["questions"] == []

    invalid = client.post(
        "/api/learning/review-sessions",
        headers=headers,
        json={"source_types": ["notes", "notes"]},
    )
    assert invalid.status_code == 422


def test_review_session_uses_deepseek_selection_and_accepted_answers(client):
    headers = seed_note_progress(client)
    grant_ai_review_generation(client)

    class FakeReviewQuestionGenerator:
        provider = "deepseek"
        model = "deepseek-chat"

        def __init__(self):
            self.received_sources = []

        def generate(self, candidates, limit):
            self.received_sources = [candidate.source_type for candidate in candidates]
            return ReviewSelection(
                plans=(
                    ReviewQuestionPlan(
                        candidate_id=0,
                        accepted_answers=("Could you wait a moment?",),
                        explanation="请对方稍等片刻。",
                    ),
                ),
                provider=self.provider,
                model=self.model,
            )

    generator = FakeReviewQuestionGenerator()
    client.app.state.review_question_generator = generator
    session = client.post(
        "/api/learning/review-sessions",
        headers=headers,
        json={"days": 7, "limit": 1, "source_types": ["notes"]},
    )
    assert session.status_code == 201
    payload = session.json()
    assert payload["generation"] == {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "fallback": False,
    }
    assert set(generator.received_sources) == {"english_note_item"}
    question = payload["questions"][0]
    assert question["prompt"] == "你能等我一下吗？"
    assert "correct_answer" not in question

    graded = client.post(
        f"/api/learning/review-sessions/{payload['id']}/answers",
        headers=headers,
        json={
            "question_id": question["id"],
            "answer": "Could you wait a moment",
        },
    )
    assert graded.status_code == 200
    assert graded.json()["is_correct"] is True
    assert graded.json()["correct_answer"] == "Could you wait for me?"
    assert graded.json()["explanation"] == "请对方稍等片刻。"


def test_review_session_uses_deterministic_selection_without_ai_benefit(client):
    headers = seed_note_progress(client)
    grant_membership_without_ai_review_generation(client)

    class FakeReviewQuestionGenerator:
        def generate(self, candidates, limit):
            raise AssertionError("AI generation must not run without its membership benefit")

    client.app.state.review_question_generator = FakeReviewQuestionGenerator()
    session = client.post(
        "/api/learning/review-sessions",
        headers=headers,
        json={"days": 7, "limit": 1, "source_types": ["notes"]},
    )

    assert session.status_code == 201
    assert session.json()["generation"] == {
        "provider": "deterministic",
        "model": "",
        "fallback": True,
    }
    assert session.json()["questions"]


def test_deepseek_review_generator_uses_openai_compatible_contract():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(
            200,
            request=request,
            json={
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "questions": [
                                        {
                                            "candidate_id": 0,
                                            "accepted_answers": [
                                                "Could you wait for me?",
                                                "Could you wait a moment?",
                                            ],
                                            "explanation": "用于请对方稍等。",
                                        }
                                    ]
                                },
                                ensure_ascii=False,
                            )
                        }
                    }
                ]
            },
        )

    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-not-for-production-123",
        deepseek_api_key="test-deepseek-key",
        deepseek_base_url="https://api.deepseek.test/v1",
        deepseek_review_model="deepseek-chat",
    )
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    generator = DeepSeekReviewQuestionGenerator(settings, client=http_client)
    selection = generator.generate(
        [
            ReviewCandidate(
                source_type="english_note_item",
                source_id=1,
                source_parent_id=1,
                source_label="英语笔记 · Daily practice",
                source_locator="example-1",
                english="Could you wait for me?",
                chinese="你能等我一下吗？",
                explanation="用于请对方稍等。",
            )
        ],
        limit=1,
    )

    assert selection is not None
    assert selection.provider == "deepseek"
    assert selection.plans[0].accepted_answers[1] == "Could you wait a moment?"
    request = requests[0]
    assert request.url == "https://api.deepseek.test/v1/chat/completions"
    assert request.headers["Authorization"] == "Bearer test-deepseek-key"
    body = json.loads(request.content)
    assert body["model"] == "deepseek-chat"
    assert body["response_format"] == {"type": "json_object"}
    assert body["messages"][0]["role"] == "system"


def test_review_logs_do_not_copy_prompts_or_submitted_answers():
    assert _redact_review_request(
        "/api/learning/review-sessions",
        {"days": 7, "limit": 10, "source_types": ["notes"]},
    ) == {"days": 7, "limit": 10, "source_types": ["notes"]}
    assert _redact_review_request(
        "/api/learning/review-sessions/hei1_session/answers",
        {
            "question_id": 9,
            "answer": "Could you wait for me?",
        },
    ) == {
        "omitted": "review answer",
        "has_question_id": True,
    }
