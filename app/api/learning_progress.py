"""HTTP controllers for course progress and learning-time sessions."""

from datetime import date

from fastapi import APIRouter, Query

from app.api.dependencies import Db, User
from app.schemas import (
    LearningCourseProgressInput,
    LearningStudySessionFinishInput,
    LearningStudySessionStartInput,
)
from app.services.learning_progress import LearningProgressService, LearningStudySessionService

router = APIRouter(tags=["learning-progress"])


@router.get("/learning/progress")
def list_progress(db: Db, user: User):
    return LearningProgressService(db).list_for_user(user["id"])


@router.get("/learning/progress/continue")
def continue_learning(db: Db, user: User):
    return LearningProgressService(db).continue_learning(user["id"])


@router.post("/learning/progress")
def save_progress(data: LearningCourseProgressInput, db: Db, user: User):
    return LearningProgressService(db).save(user, data)


@router.get("/learning/study-sessions")
def list_study_sessions(db: Db, user: User):
    return LearningStudySessionService(db).list_for_user(user["id"])


@router.post("/learning/study-sessions", status_code=201)
def start_study_session(data: LearningStudySessionStartInput, db: Db, user: User):
    return LearningStudySessionService(db).start(user, data)


@router.put("/learning/study-sessions/{session_id}/finish")
def finish_study_session(
    session_id: int,
    data: LearningStudySessionFinishInput,
    db: Db,
    user: User,
):
    return LearningStudySessionService(db).finish(user, session_id, data)


@router.get("/learning/study-time")
def study_time(
    db: Db,
    user: User,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):
    return LearningStudySessionService(db).time_summary(user["id"], start_date, end_date)
