"""HTTP controller for the study_progress table."""

from fastapi import APIRouter, Query

from app.api.dependencies import Db, User
from app.schemas import ProgressInput
from app.services.progress import StudyProgressService

router = APIRouter(tags=["study-progress"])


@router.get("/progress")
def list_progress(db: Db, user: User):
    return StudyProgressService(db).list_for_user(user["id"])


@router.get("/learning/review-items")
def recent_review_items(
    db: Db,
    user: User,
    days: int = Query(default=7, ge=1, le=30),
    limit: int = Query(default=3, ge=1, le=6),
):
    return StudyProgressService(db).recent_review_items(user, days, limit)


@router.post("/progress")
def save_progress(data: ProgressInput, db: Db, user: User):
    return StudyProgressService(db).save(user, data)
