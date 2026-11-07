"""Persistence for the water-sort campaign; each user's actions are serialized."""

from sqlalchemy import select

from app import models as m
from app.dao.base import BaseTableDAO


class WaterSortProgressDAO(BaseTableDAO):
    table = m.game_water_sort_progress

    def lock_user(self, user_id):
        # Lock an existing row even before the user's first progress record exists.
        self.db.execute(select(m.user.c.id).where(m.user.c.id == user_id).with_for_update()).first()

    def for_user(self, user_id):
        # MySQL's default REPEATABLE READ may already have an authentication
        # snapshot. A locking/current read must see the previous action's commit.
        return self.db.execute(select(self.table).where(self.table.c.user_id == user_id).with_for_update()).mappings().first()


class WaterSortAttemptDAO(BaseTableDAO):
    table = m.game_water_sort_attempt

    def for_user(self, attempt_id, user_id):
        return self.db.execute(select(self.table).where(
            self.table.c.id == attempt_id, self.table.c.user_id == user_id
        ).with_for_update()).mappings().first()


WATER_SORT_TABLE_DAO_TYPES = {
    "game_water_sort_progress": WaterSortProgressDAO,
    "game_water_sort_attempt": WaterSortAttemptDAO,
}
