from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models as m
from app.dao.vocabulary import (
    UserVocabularyProgressDAO,
    VocabularyDeckDAO,
    VocabularyReviewLogDAO,
    VocabularyWordDAO,
)
from app.services.vocabulary import UserVocabularyProgressService
from tests.support import sample_engine


def _insert_card(db):
    deck_id = db.execute(
        m.vocabulary_deck.insert().values(
            deck_code="software-english-test",
            title="技术英语测试词库",
            category="技术英语",
            sort_order=10,
            is_published=1,
        )
    ).inserted_primary_key[0]
    word_id = db.execute(
        m.vocabulary_word.insert().values(
            word="refine",
            normalized_word="refine",
            phonetic_uk="/rɪˈfaɪn/",
            is_active=1,
        )
    ).inserted_primary_key[0]
    sense_id = db.execute(
        m.vocabulary_word_sense.insert().values(
            word_id=word_id,
            part_of_speech="verb",
            translation="完善；提炼",
            definition="通过小幅调整，让内容或方案变得更好。",
            memory_hint="反复打磨，让内容更精细。",
            sort_order=1,
        )
    ).inserted_primary_key[0]
    db.execute(
        m.vocabulary_word_example.insert().values(
            sense_id=sense_id,
            english_text="We need to refine the design before launch.",
            chinese_text="我们需要在上线前完善这个设计。",
            sort_order=1,
        )
    )
    deck_word_id = db.execute(
        m.vocabulary_deck_word.insert().values(
            deck_id=deck_id,
            word_id=word_id,
            sort_order=10,
            is_enabled=1,
        )
    ).inserted_primary_key[0]
    db.commit()
    return deck_id, word_id, deck_word_id


def test_vocabulary_deck_and_word_queries_return_card_details():
    engine = sample_engine()
    with Session(engine) as db:
        deck_id, word_id, deck_word_id = _insert_card(db)

        decks = VocabularyDeckDAO(db).list_library(user_id=2)
        assert [(deck["deck_code"], deck["word_count"]) for deck in decks] == [
            ("software-english-test", 1)
        ]

        cards = VocabularyDeckDAO(db).list_study_cards(deck_id, user_id=2)
        assert len(cards) == 1
        assert cards[0]["deck_word_id"] == deck_word_id
        assert cards[0]["word"] == "refine"
        assert cards[0]["translation"] == "完善；提炼"
        assert cards[0]["example_english_text"] == "We need to refine the design before launch."
        assert cards[0]["progress_id"] is None

        detail = VocabularyWordDAO(db).detail(word_id)
        assert detail["word"]["normalized_word"] == "refine"
        assert detail["senses"][0]["examples"][0]["chinese_text"] == "我们需要在上线前完善这个设计。"
        assert [match["id"] for match in VocabularyWordDAO(db).search("ref")] == [word_id]


def test_vocabulary_progress_upsert_review_history_and_due_query():
    engine = sample_engine()
    review_time = datetime(2026, 10, 30, 9, 0, 0)
    with Session(engine) as db:
        deck_id, _, deck_word_id = _insert_card(db)
        progress = UserVocabularyProgressService(db).record_review(
            user_id=2,
            deck_word_id=deck_word_id,
            rating="review",
            duration_millis=1800,
            now=review_time,
        )

        assert progress["learning_state"] == "review"
        assert progress["mastery_level"] == 1
        assert progress["seen_count"] == 1
        assert progress["review_count"] == 1
        assert progress["next_review_at"] == review_time + timedelta(days=1)

        progress_dao = UserVocabularyProgressDAO(db)
        due_cards = progress_dao.list_due_for_user(
            2,
            deck_id=deck_id,
            now=review_time + timedelta(days=1, seconds=1),
        )
        assert [(card["deck_word_id"], card["word"]) for card in due_cards] == [
            (deck_word_id, "refine")
        ]

        marked = UserVocabularyProgressService(db).set_marked(2, deck_word_id, True)
        assert marked["is_marked"] == 1
        summary = progress_dao.deck_summary(2, deck_id)
        assert dict(summary) == {
            "total_count": 1,
            "started_count": 1,
            "mastered_count": 0,
            "marked_count": 1,
        }

        history = VocabularyReviewLogDAO(db).list_for_user_card(2, deck_word_id)
        assert len(history) == 1
        assert history[0]["rating"] == "review"
        assert history[0]["duration_millis"] == 1800
