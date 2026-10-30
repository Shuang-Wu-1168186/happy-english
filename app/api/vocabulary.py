"""Learner-facing API for the vocabulary-memory training flow."""

from fastapi import APIRouter, Query

from app.api.dependencies import Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.schemas import VocabularyCardMarkInput, VocabularyReviewInput
from app.services.vocabulary import VocabularyMemoryService


router = APIRouter(tags=["vocabulary-memory"], route_class=OpaqueIdRoute)


@router.get("/learning/vocabulary/decks")
def list_vocabulary_decks(db: Db, user: User):
    return VocabularyMemoryService(db).list_decks(user)


@router.get("/learning/vocabulary/decks/{deck_id}")
def get_vocabulary_deck(deck_id: int, db: Db, user: User):
    return VocabularyMemoryService(db).get_deck(user, deck_id)


@router.get("/learning/vocabulary/decks/{deck_id}/cards")
def list_vocabulary_cards(deck_id: int, db: Db, user: User):
    return VocabularyMemoryService(db).list_cards(user, deck_id)


@router.get("/learning/vocabulary/decks/{deck_id}/review-cards")
def list_due_vocabulary_cards(
    deck_id: int,
    db: Db,
    user: User,
    limit: int = Query(default=30, ge=1, le=100),
):
    return VocabularyMemoryService(db).list_due_cards(user, deck_id, limit)


@router.get("/learning/vocabulary/decks/{deck_id}/progress")
def get_vocabulary_deck_progress(deck_id: int, db: Db, user: User):
    return VocabularyMemoryService(db).get_deck(user, deck_id)


@router.get("/learning/vocabulary/words/{word_id}")
def get_vocabulary_word(word_id: int, db: Db, user: User):
    return VocabularyMemoryService(db).get_word(word_id)


@router.post("/learning/vocabulary/cards/{card_id}/reviews")
def record_vocabulary_review(
    card_id: int,
    payload: VocabularyReviewInput,
    db: Db,
    user: User,
):
    return VocabularyMemoryService(db).record_review(
        user,
        card_id,
        payload.rating,
        payload.duration_millis,
    )


@router.put("/learning/vocabulary/cards/{card_id}/mark")
def set_vocabulary_card_mark(
    card_id: int,
    payload: VocabularyCardMarkInput,
    db: Db,
    user: User,
):
    return VocabularyMemoryService(db).set_marked(user, card_id, payload.is_marked)


@router.get("/learning/vocabulary/cards/{card_id}/review-history")
def list_vocabulary_review_history(
    card_id: int,
    db: Db,
    user: User,
    limit: int = Query(default=100, ge=1, le=100),
):
    return VocabularyMemoryService(db).review_history(user, card_id, limit)
