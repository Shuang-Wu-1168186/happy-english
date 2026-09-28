"""DAOs for course progress, item progress, and study-session records."""

from datetime import datetime, time, timedelta

from sqlalchemy import func, select

from app import models as m
from app.dao.base import BaseTableDAO


class LearningProgressDAO(BaseTableDAO):
    table = m.learning_progress

    def find_for_user_course(self, user_id, course_id):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.user_id == user_id,
                    self.table.c.course_id == course_id,
                )
            )
            .mappings()
            .first()
        )

    def list_for_user(self, user_id, limit=50):
        course = m.learning_course
        return (
            self.db.execute(
                select(
                    self.table,
                    course.c.title.label("course_title"),
                    course.c.title_en.label("course_title_en"),
                    course.c.cover_url.label("course_cover_url"),
                    course.c.course_type,
                    course.c.content_resource.label("course_content_resource"),
                    course.c.content_reference_id.label("course_content_reference_id"),
                )
                .join(course, course.c.id == self.table.c.course_id)
                .where(self.table.c.user_id == user_id, course.c.is_published == 1)
                .order_by(self.table.c.last_studied_at.desc(), self.table.c.id.desc())
                .limit(limit)
            )
            .mappings()
            .all()
        )

    def add_study_seconds(self, progress_id, seconds):
        self.db.execute(
            self.table.update()
            .where(self.table.c.id == progress_id)
            .values(
                accumulated_seconds=func.coalesce(self.table.c.accumulated_seconds, 0) + seconds,
                last_studied_at=func.now(),
                updated_at=func.now(),
            )
        )


class LearningProgressItemDAO(BaseTableDAO):
    table = m.learning_progress_item

    def find_for_progress_item(self, progress_id, item_key):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.progress_id == progress_id,
                    self.table.c.item_key == item_key,
                )
            )
            .mappings()
            .first()
        )

    def count_completed(self, progress_id):
        return self.count(
            self.table.c.progress_id == progress_id,
            self.table.c.is_completed == 1,
        )

    def list_for_progress(self, progress_id):
        return self.list_where(
            self.table.c.progress_id == progress_id,
            order_by=[self.table.c.last_studied_at.desc(), self.table.c.id.desc()],
        )


class LearningStudySessionDAO(BaseTableDAO):
    table = m.learning_study_session

    def get_for_user(self, session_id, user_id):
        return self.find_by_id(session_id, self.table.c.user_id == user_id)

    def find_open_for_user_course(self, user_id, course_id):
        return (
            self.db.execute(
                select(self.table)
                .where(
                    self.table.c.user_id == user_id,
                    self.table.c.course_id == course_id,
                    self.table.c.ended_at.is_(None),
                )
                .order_by(self.table.c.started_at.desc(), self.table.c.id.desc())
            )
            .mappings()
            .first()
        )

    def list_for_user(self, user_id, limit=50):
        return (
            self.db.execute(
                select(self.table)
                .where(self.table.c.user_id == user_id)
                .order_by(self.table.c.started_at.desc(), self.table.c.id.desc())
                .limit(limit)
            )
            .mappings()
            .all()
        )

    def time_summary(self, user_id, start_date=None, end_date=None):
        filters = [self.table.c.user_id == user_id, self.table.c.ended_at.is_not(None)]
        if start_date:
            filters.append(self.table.c.started_at >= datetime.combine(start_date, time.min))
        if end_date:
            filters.append(self.table.c.started_at < datetime.combine(end_date + timedelta(days=1), time.min))
        study_date = func.date(self.table.c.started_at).label("study_date")
        daily = (
            self.db.execute(
                select(
                    study_date,
                    func.coalesce(func.sum(self.table.c.active_seconds), 0).label("active_seconds"),
                    func.count().label("session_count"),
                )
                .where(*filters)
                .group_by(study_date)
                .order_by(study_date)
            )
            .mappings()
            .all()
        )
        total = self.db.scalar(
            select(func.coalesce(func.sum(self.table.c.active_seconds), 0)).where(*filters)
        )
        return {"total_active_seconds": total or 0, "days": daily}


LEARNING_PROGRESS_TABLE_DAO_TYPES = {
    m.learning_progress.name: LearningProgressDAO,
    m.learning_progress_item.name: LearningProgressItemDAO,
    m.learning_study_session.name: LearningStudySessionDAO,
}
