"""Business rules for course progress and learning-time session records."""

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func

from app import schemas as s
from app.dao.learning_progress import (
    LearningProgressDAO,
    LearningProgressItemDAO,
    LearningStudySessionDAO,
)
from app.services.learning_catalog import LearningCourseService, serialise_catalog


def serialise_progress(row):
    """Add the derived percentage without storing a second, conflicting value."""
    result = dict(row)
    total = result.get("total_item_count") or 0
    completed = result.get("completed_item_count") or 0
    result["progress_percent"] = round(completed * 100 / total, 1) if total else 0
    return result


class LearningProgressService:
    """Course-level progress and resume-position rules."""

    def __init__(self, db):
        self.db = db
        self.dao = LearningProgressDAO(db)
        self.item_dao = LearningProgressItemDAO(db)
        self.course_service = LearningCourseService(db)

    def require_course(self, course_id, user=None):
        course = self.course_service.require_public(course_id)
        if user is not None:
            # Import here to keep the catalogue and entitlement services free of
            # module-level circular imports.
            from app.services.membership import LearningUserCourseService

            access = LearningUserCourseService(self.db).course_access(user["id"], course)
            if access["access_state"] != "available":
                raise HTTPException(403, "This course requires an active membership benefit.")
        return course

    def ensure_for_course(self, user, course_id, course=None):
        course = course or self.require_course(course_id)
        progress = self.dao.find_for_user_course(user["id"], course["id"])
        if progress:
            return progress, course
        progress_id = self.dao.insert(
            {
                "user_id": user["id"],
                "course_id": course["id"],
                "status": "in_progress",
                "last_studied_at": func.now(),
            }
        )
        return self.dao.find_by_id(progress_id), course

    def _response(self, progress, course=None):
        result = serialise_progress(progress)
        if course:
            result["course"] = serialise_catalog(course)
        return result

    def list_for_user(self, user_id):
        return {"items": [serialise_progress(row) for row in self.dao.list_for_user(user_id)]}

    def continue_learning(self, user_id):
        rows = self.dao.list_for_user(user_id, limit=1)
        return serialise_progress(rows[0]) if rows else None

    def _record_item(self, progress_id, item):
        existing = self.item_dao.find_for_progress_item(progress_id, item.item_key)
        attempted = int(item.is_completed or item.score is not None)
        values = {
            "item_type": item.item_type,
            "item_reference_id": item.item_reference_id,
            "is_completed": int(item.is_completed),
            "last_position_seconds": item.last_position_seconds,
            "score": item.score,
            "last_studied_at": func.now(),
            "completed_at": func.now() if item.is_completed else None,
        }
        if existing:
            values["attempt_count"] = existing["attempt_count"] + attempted
            self.item_dao.update(existing["id"], values)
        else:
            self.item_dao.insert(
                {
                    **values,
                    "progress_id": progress_id,
                    "item_key": item.item_key,
                    "attempt_count": attempted,
                }
            )

    def save(self, user, data: s.LearningCourseProgressInput):
        course = self.require_course(data.course_id, user)
        progress, _ = self.ensure_for_course(user, data.course_id, course)
        if data.item:
            self._record_item(progress["id"], data.item)

        completed_items = self.item_dao.count_completed(progress["id"])
        total_items = (
            data.total_item_count if data.total_item_count is not None else progress["total_item_count"]
        )
        if data.completed is not None:
            status = "completed" if data.completed else "in_progress"
        elif total_items:
            status = "completed" if completed_items >= total_items else "in_progress"
        else:
            status = progress["status"]

        values = {
            "status": status,
            "total_item_count": total_items,
            "completed_item_count": completed_items,
            "last_studied_at": func.now(),
        }
        if data.last_item_key is not None:
            values["last_item_key"] = data.last_item_key
        elif data.item:
            values["last_item_key"] = data.item.item_key
        if data.last_item_id is not None:
            values["last_item_id"] = data.last_item_id
        elif data.item and data.item.item_reference_id is not None:
            values["last_item_id"] = data.item.item_reference_id
        if data.last_position_seconds is not None:
            values["last_position_seconds"] = data.last_position_seconds
        elif data.item:
            values["last_position_seconds"] = data.item.last_position_seconds
        if status == "completed":
            if progress["status"] != "completed":
                values["completed_at"] = func.now()
        else:
            values["completed_at"] = None
        self.dao.update(progress["id"], values)
        self.db.commit()
        return self._response(self.dao.find_by_id(progress["id"]), course)


class LearningProgressItemService:
    """Per-item progress service used by the course progress aggregate."""

    dao_type = LearningProgressItemDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def list_for_progress(self, progress_id):
        return [dict(row) for row in self.dao.list_for_progress(progress_id)]


class LearningStudySessionService:
    """Append-only study sessions used to calculate actual learning time."""

    dao_type = LearningStudySessionDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)
        self.progress = LearningProgressService(db)

    def start(self, user, data: s.LearningStudySessionStartInput):
        course = self.progress.require_course(data.course_id, user)
        progress, _ = self.progress.ensure_for_course(user, data.course_id, course)
        existing = self.dao.find_open_for_user_course(user["id"], data.course_id)
        if existing:
            return {**dict(existing), "reused": True}
        session_id = self.dao.insert(
            {
                "user_id": user["id"],
                "progress_id": progress["id"],
                "course_id": data.course_id,
                "platform": data.platform,
                "entry_source": data.entry_source or None,
            }
        )
        self.db.commit()
        return {**dict(self.dao.find_by_id(session_id)), "reused": False}

    def finish(self, user, session_id, data: s.LearningStudySessionFinishInput):
        session = self.dao.get_for_user(session_id, user["id"])
        if not session:
            raise HTTPException(404, "Learning session not found.")
        if session["ended_at"] is not None:
            return dict(session)

        now = datetime.now(session["started_at"].tzinfo)
        elapsed_seconds = max(0, int((now - session["started_at"]).total_seconds()))
        active_seconds = (
            elapsed_seconds if data.active_seconds is None else min(data.active_seconds, elapsed_seconds + 5)
        )
        self.dao.update(
            session_id,
            {
                "ended_at": now,
                "last_heartbeat_at": now,
                "active_seconds": active_seconds,
            },
        )
        self.progress.dao.add_study_seconds(session["progress_id"], active_seconds)
        self.db.commit()
        return dict(self.dao.find_by_id(session_id))

    def list_for_user(self, user_id):
        return {"items": [dict(row) for row in self.dao.list_for_user(user_id)]}

    def time_summary(self, user_id, start_date=None, end_date=None):
        result = self.dao.time_summary(user_id, start_date, end_date)
        return {**result, "days": [dict(row) for row in result["days"]]}


LEARNING_PROGRESS_TABLE_SERVICE_TYPES = {
    "learning_progress": LearningProgressService,
    "learning_progress_item": LearningProgressItemService,
    "learning_study_session": LearningStudySessionService,
}
