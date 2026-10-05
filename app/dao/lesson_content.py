"""DAOs for the generic lesson section, item, and source model."""

from app import models as m
from app.dao.base import BaseTableDAO


class LearningLessonSectionDAO(BaseTableDAO):
    table = m.learning_lesson_section

    def list_for_lesson(self, lesson_id, published_only=False):
        conditions = [self.table.c.lesson_id == lesson_id]
        if published_only:
            conditions.append(self.table.c.status == "published")
        return self.list_where(*conditions, order_by=(self.table.c.sort_order, self.table.c.id))


class LearningLessonItemDAO(BaseTableDAO):
    table = m.learning_lesson_item

    def list_for_section(self, section_id, published_only=False):
        conditions = [self.table.c.section_id == section_id]
        if published_only:
            conditions.append(self.table.c.status == "published")
        return self.list_where(*conditions, order_by=(self.table.c.item_order, self.table.c.id))


LESSON_CONTENT_TABLE_DAO_TYPES = {
    m.learning_lesson_section.name: LearningLessonSectionDAO,
    m.learning_lesson_item.name: LearningLessonItemDAO,
}
