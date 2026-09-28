"""Persistence access for courseware blocks and their immutable source snapshots."""

from app import models as m
from app.dao.base import BaseTableDAO


class CoursewareBlockDAO(BaseTableDAO):
    table = m.courseware_block

    def list_for_lesson(self, lesson_id, published_only=False):
        conditions = [self.table.c.material_lesson_id == lesson_id]
        if published_only:
            conditions.append(self.table.c.status == "published")
        return self.list_where(*conditions, order_by=(self.table.c.sort_order, self.table.c.id))


class CoursewareBlockSourceDAO(BaseTableDAO):
    table = m.courseware_block_source

    def list_for_block(self, block_id):
        return self.list_where(
            self.table.c.courseware_block_id == block_id,
            order_by=(self.table.c.sort_order, self.table.c.id),
        )


COURSEWARE_TABLE_DAO_TYPES = {
    m.courseware_block.name: CoursewareBlockDAO,
    m.courseware_block_source.name: CoursewareBlockSourceDAO,
}
