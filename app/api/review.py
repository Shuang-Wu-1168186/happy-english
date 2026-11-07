"""Learner-facing active-recall review endpoints."""

from fastapi import APIRouter, Request

from app.api.dependencies import Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.schemas import LearningReviewAnswerInput, LearningReviewSessionInput
from app.services.review import LearningReviewSessionService


router = APIRouter(tags=["learning-review"], route_class=OpaqueIdRoute)


@router.post("/learning/review-sessions", status_code=201)
def create_review_session(
    payload: LearningReviewSessionInput,
    request: Request,
    db: Db,
    user: User,
):
    return LearningReviewSessionService(
        db,
        question_generator=request.app.state.review_question_generator,
    ).create(user, payload)


@router.get("/learning/review-sessions/{session_id}")
def get_review_session(session_id: int, db: Db, user: User):
    return LearningReviewSessionService(db).get(user, session_id)


@router.post("/learning/review-sessions/{session_id}/answers")
def submit_review_answer(
    session_id: int,
    payload: LearningReviewAnswerInput,
    db: Db,
    user: User,
):
    return LearningReviewSessionService(db).submit_answer(user, session_id, payload)
