"""DAO for the study_progress table."""

from sqlalchemy import func, select

from app import models as m
from app.dao.base import BaseTableDAO


class StudyProgressDAO(BaseTableDAO):
    table = m.study_progress

    def list_for_user(self, user_id):
        return (
            self.db.execute(
                select(self.table)
                .where(self.table.c.user_id == user_id)
                .order_by(self.table.c.last_studied_at.desc())
            )
            .mappings()
            .all()
        )

    def list_recent_for_user(self, user_id, since, limit=100):
        return (
            self.db.execute(
                select(self.table)
                .where(
                    self.table.c.user_id == user_id,
                    self.table.c.last_studied_at >= since,
                )
                .order_by(self.table.c.last_studied_at.desc(), self.table.c.id.desc())
                .limit(limit)
            )
            .mappings()
            .all()
        )

    def delete_for_parent(self, content_type, parent_id):
        self.delete_where(
            self.table.c.content_type == content_type,
            self.table.c.parent_id == parent_id,
        )

    def delete_for_item(self, content_type, item_id):
        self.delete_where(
            self.table.c.content_type == content_type,
            self.table.c.item_id == item_id,
        )

    def save(self, values):
        dialect = self.db.get_bind().dialect.name
        if dialect == "mysql":
            from sqlalchemy.dialects.mysql import insert

            statement = (
                insert(self.table)
                .values(**values)
                .on_duplicate_key_update(
                    item_id=values["item_id"],
                    completed=values["completed"],
                    last_studied_at=func.now(),
                    updated_at=func.now(),
                )
            )
        else:
            from sqlalchemy.dialects.sqlite import insert

            statement = (
                insert(self.table)
                .values(**values)
                .on_conflict_do_update(
                    index_elements=["user_id", "content_type", "parent_id"],
                    set_={
                        "item_id": values["item_id"],
                        "completed": values["completed"],
                        "last_studied_at": func.now(),
                        "updated_at": func.now(),
                    },
                )
            )
        self.db.execute(statement)


STUDY_PROGRESS_TABLE_DAO_TYPES = {
    m.study_progress.name: StudyProgressDAO,
}
