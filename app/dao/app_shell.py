"""Persistence helpers for server-authored application presentation settings."""

from sqlalchemy import case, select

from app import models as m
from app.dao.base import BaseTableDAO


class AppPresentationConfigDAO(BaseTableDAO):
    table = m.app_presentation_config

    def by_target(self, target_type, target_key, platform):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.target_type == target_type,
                    self.table.c.target_key == target_key,
                    self.table.c.platform == platform,
                )
            )
            .mappings()
            .first()
        )

    def effective_for(self, target_type, target_key, platform):
        """Prefer an exact platform configuration, then use the all-platform one."""

        return (
            self.db.execute(
                select(self.table)
                .where(
                    self.table.c.target_type == target_type,
                    self.table.c.target_key == target_key,
                    self.table.c.status == "active",
                    self.table.c.platform.in_((platform, "all")),
                )
                .order_by(
                    case((self.table.c.platform == platform, 0), else_=1),
                    self.table.c.sort_order,
                    self.table.c.id,
                )
            )
            .mappings()
            .first()
        )

    def list_all(self):
        return self.list_where(order_by=[self.table.c.target_type, self.table.c.target_key, self.table.c.platform])


APP_SHELL_TABLE_DAO_TYPES = {
    m.app_presentation_config.name: AppPresentationConfigDAO,
}
