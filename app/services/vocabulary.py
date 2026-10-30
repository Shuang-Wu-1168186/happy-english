"""Vocabulary-memory persistence and learner-facing use cases."""

from datetime import timedelta

from fastapi import HTTPException

from app.core.time import utc_now_naive
from app.dao.vocabulary import (
    UserVocabularyProgressDAO,
    VocabularyDeckDAO,
    VocabularyDeckWordDAO,
    VocabularyReviewLogDAO,
    VocabularyWordDAO,
    VocabularyWordExampleDAO,
    VocabularyWordSenseDAO,
)


class VocabularyTableService:
    """Small common wrapper for services registered for vocabulary tables."""

    dao_type = None

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class VocabularyDeckService(VocabularyTableService):
    dao_type = VocabularyDeckDAO


class VocabularyWordService(VocabularyTableService):
    dao_type = VocabularyWordDAO


class VocabularyWordSenseService(VocabularyTableService):
    dao_type = VocabularyWordSenseDAO


class VocabularyWordExampleService(VocabularyTableService):
    dao_type = VocabularyWordExampleDAO


class VocabularyDeckWordService(VocabularyTableService):
    dao_type = VocabularyDeckWordDAO


class UserVocabularyProgressService(VocabularyTableService):
    """Persist the three ratings used by the word-memory card interaction."""

    dao_type = UserVocabularyProgressDAO
    _rating_rules = {
        "repeat": ("learning", -1, timedelta(minutes=10)),
        "review": ("review", 1, timedelta(days=1)),
        "mastered": ("mastered", 2, timedelta(days=4)),
    }

    def __init__(self, db):
        super().__init__(db)
        self.review_logs = VocabularyReviewLogDAO(db)

    def record_review(self, user_id, deck_word_id, rating, duration_millis=None, now=None):
        """Update the current card state and retain one immutable review event."""

        try:
            learning_state, mastery_delta, interval = self._rating_rules[rating]
        except KeyError as error:
            raise ValueError(f"Unknown vocabulary rating: {rating}") from error
        reviewed_at = now or utc_now_naive()
        existing = self.dao.find_for_user_card(user_id, deck_word_id)
        previous_mastery = int(existing["mastery_level"]) if existing else 0
        mastery_level = min(5, max(0, previous_mastery + mastery_delta))
        self.dao.upsert(
            {
                "user_id": user_id,
                "deck_word_id": deck_word_id,
                "learning_state": learning_state,
                "mastery_level": mastery_level,
                "is_marked": existing["is_marked"] if existing else 0,
                "seen_count": (existing["seen_count"] if existing else 0) + 1,
                "review_count": (existing["review_count"] if existing else 0) + 1,
                "correct_count": (existing["correct_count"] if existing else 0)
                + int(rating == "mastered"),
                "last_rating": rating,
                "last_reviewed_at": reviewed_at,
                "next_review_at": reviewed_at + interval,
            }
        )
        self.review_logs.record(
            {
                "user_id": user_id,
                "deck_word_id": deck_word_id,
                "rating": rating,
                "previous_mastery_level": previous_mastery,
                "mastery_level": mastery_level,
                "duration_millis": duration_millis,
                "reviewed_at": reviewed_at,
                "next_review_at": reviewed_at + interval,
            }
        )
        self.db.commit()
        return self.dao.find_for_user_card(user_id, deck_word_id)

    def set_marked(self, user_id, deck_word_id, is_marked):
        progress = self.dao.set_marked(user_id, deck_word_id, is_marked)
        self.db.commit()
        return progress


class VocabularyReviewLogService(VocabularyTableService):
    dao_type = VocabularyReviewLogDAO


class VocabularyMemoryService:
    """Expose published vocabulary decks without trusting client-owned progress."""

    def __init__(self, db):
        self.db = db
        self.decks = VocabularyDeckDAO(db)
        self.words = VocabularyWordDAO(db)
        self.deck_words = VocabularyDeckWordDAO(db)
        self.progress = UserVocabularyProgressService(db)
        self.review_logs = VocabularyReviewLogDAO(db)

    @staticmethod
    def _progress_view(progress):
        if not progress:
            return None
        return {
            "id": progress["id"],
            "learning_state": progress["learning_state"],
            "mastery_level": progress["mastery_level"],
            "is_marked": bool(progress["is_marked"]),
            "seen_count": progress["seen_count"],
            "review_count": progress["review_count"],
            "correct_count": progress["correct_count"],
            "last_rating": progress["last_rating"],
            "last_reviewed_at": progress["last_reviewed_at"],
            "next_review_at": progress["next_review_at"],
        }

    @classmethod
    def _card_view(cls, card):
        progress_id = card.get("progress_id")
        progress = None
        if progress_id is not None:
            progress = cls._progress_view(
                {
                    "id": progress_id,
                    "learning_state": card["learning_state"],
                    "mastery_level": card["mastery_level"],
                    "is_marked": card["is_marked"],
                    "seen_count": card["seen_count"],
                    "review_count": card["review_count"],
                    "correct_count": card["correct_count"],
                    "last_rating": card["last_rating"],
                    "last_reviewed_at": card["last_reviewed_at"],
                    "next_review_at": card["next_review_at"],
                }
            )
        sense = None
        if card.get("sense_id") is not None:
            sense = {
                "id": card["sense_id"],
                "part_of_speech": card["part_of_speech"],
                "translation": card["translation"],
                "definition": card["definition"],
                "memory_hint": card["memory_hint"],
            }
        example = None
        if card.get("example_id") is not None:
            example = {
                "id": card["example_id"],
                "english_text": card["example_english_text"],
                "chinese_text": card["example_chinese_text"],
            }
        return {
            "card_id": card["deck_word_id"],
            "deck_id": card["deck_id"],
            "sort_order": card["card_sort_order"],
            "word": {
                "id": card["word_id"],
                "word": card["word"],
                "normalized_word": card["normalized_word"],
                "phonetic_uk": card["phonetic_uk"],
                "phonetic_us": card["phonetic_us"],
                "audio_url": card["audio_url"],
                "word_level": card["word_level"],
            },
            "sense": sense,
            "example": example,
            "progress": progress,
        }

    @staticmethod
    def _review_view(review):
        return {
            "id": review["id"],
            "card_id": review["deck_word_id"],
            "rating": review["rating"],
            "previous_mastery_level": review["previous_mastery_level"],
            "mastery_level": review["mastery_level"],
            "duration_millis": review["duration_millis"],
            "reviewed_at": review["reviewed_at"],
            "next_review_at": review["next_review_at"],
        }

    def _require_published_deck(self, deck_id):
        deck = self.decks.find_by_id(deck_id)
        if not deck or not deck["is_published"]:
            raise HTTPException(404, "Vocabulary deck not found.")
        return deck

    def _require_active_card(self, card_id):
        card = self.deck_words.find_by_id(card_id)
        if not card or not card["is_enabled"]:
            raise HTTPException(404, "Vocabulary card not found.")
        self._require_published_deck(card["deck_id"])
        word = self.words.find_by_id(card["word_id"])
        if not word or not word["is_active"]:
            raise HTTPException(404, "Vocabulary card not found.")
        return card

    def _require_public_word(self, word_id):
        word = self.words.find_by_id(word_id)
        if not word or not word["is_active"] or not self.deck_words.find_published_for_word(word_id):
            raise HTTPException(404, "Vocabulary word not found.")
        return word

    def _summary(self, user_id, deck_id):
        return dict(self.progress.dao.deck_summary(user_id, deck_id))

    def list_decks(self, user):
        return {"items": [dict(deck) for deck in self.decks.list_library(user["id"])]}

    def get_deck(self, user, deck_id):
        deck = self._require_published_deck(deck_id)
        return {"deck": dict(deck), "summary": self._summary(user["id"], deck_id)}

    def list_cards(self, user, deck_id):
        deck = self._require_published_deck(deck_id)
        cards = self.decks.list_study_cards(deck_id, user["id"])
        return {
            "deck": dict(deck),
            "summary": self._summary(user["id"], deck_id),
            "items": [self._card_view(card) for card in cards],
        }

    def list_due_cards(self, user, deck_id, limit):
        deck = self._require_published_deck(deck_id)
        cards_by_id = {
            card["deck_word_id"]: self._card_view(card)
            for card in self.decks.list_study_cards(deck_id, user["id"])
        }
        due_rows = self.progress.dao.list_due_for_user(user["id"], deck_id, limit=limit)
        return {
            "deck": dict(deck),
            "summary": self._summary(user["id"], deck_id),
            "items": [
                cards_by_id[row["deck_word_id"]]
                for row in due_rows
                if row["deck_word_id"] in cards_by_id
            ],
        }

    def get_word(self, word_id):
        self._require_public_word(word_id)
        return self.words.detail(word_id)

    def record_review(self, user, card_id, rating, duration_millis=None):
        card = self._require_active_card(card_id)
        progress = self.progress.record_review(
            user["id"],
            card_id,
            rating,
            duration_millis,
        )
        return {
            "card_id": card_id,
            "progress": self._progress_view(progress),
            "summary": self._summary(user["id"], card["deck_id"]),
        }

    def set_marked(self, user, card_id, is_marked):
        card = self._require_active_card(card_id)
        progress = self.progress.set_marked(user["id"], card_id, is_marked)
        return {
            "card_id": card_id,
            "progress": self._progress_view(progress),
            "summary": self._summary(user["id"], card["deck_id"]),
        }

    def review_history(self, user, card_id, limit):
        self._require_active_card(card_id)
        return {
            "items": [
                self._review_view(review)
                for review in self.review_logs.list_for_user_card(user["id"], card_id, limit)
            ]
        }


VOCABULARY_TABLE_SERVICE_TYPES = {
    "vocabulary_deck": VocabularyDeckService,
    "vocabulary_word": VocabularyWordService,
    "vocabulary_word_sense": VocabularyWordSenseService,
    "vocabulary_word_example": VocabularyWordExampleService,
    "vocabulary_deck_word": VocabularyDeckWordService,
    "user_vocabulary_progress": UserVocabularyProgressService,
    "vocabulary_review_log": VocabularyReviewLogService,
}
