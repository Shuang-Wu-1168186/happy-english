"""DAOs for the validated, idempotent analytics event pipeline."""

from sqlalchemy import select

from app import models as m
from app.dao.base import BaseTableDAO


class AnalyticsEventDefinitionDAO(BaseTableDAO):
    table = m.analytics_event_definition

    def by_name(self, event_name):
        return (
            self.db.execute(
                select(self.table).where(self.table.c.event_name == event_name)
            )
            .mappings()
            .first()
        )

    def list_active(self):
        return self.list_where(
            self.table.c.status == "active",
            order_by=[self.table.c.event_name, self.table.c.id],
        )

    def list_all(self):
        return self.list_where(order_by=[self.table.c.event_name, self.table.c.id])


class AnalyticsEventDAO(BaseTableDAO):
    table = m.analytics_event

    def insert_if_absent(self, values):
        """Insert exactly once across SQLite tests and the MySQL deployment."""

        dialect = self.db.bind.dialect.name
        if dialect == "sqlite":
            from sqlalchemy.dialects.sqlite import insert as dialect_insert

            result = self.db.execute(
                dialect_insert(self.table)
                .values(**values)
                .on_conflict_do_nothing(index_elements=["event_id"])
            )
            return result.rowcount == 1
        if dialect in {"mysql", "mariadb"}:
            from sqlalchemy.dialects.mysql import insert as dialect_insert

            result = self.db.execute(
                dialect_insert(self.table)
                .values(**values)
                .prefix_with("IGNORE")
            )
            return result.rowcount == 1

        if self.db.execute(
            select(self.table.c.id).where(self.table.c.event_id == values["event_id"])
        ).first():
            return False
        self.insert(values)
        return True


ANALYTICS_TABLE_DAO_TYPES = {
    m.analytics_event_definition.name: AnalyticsEventDefinitionDAO,
    m.analytics_event.name: AnalyticsEventDAO,
}
