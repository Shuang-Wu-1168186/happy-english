"""Small SQLAlchemy Core DAO primitives shared by table-specific DAOs."""

from sqlalchemy import func, select


class BaseTableDAO:
    """Persistence-only operations for one SQLAlchemy table."""

    table = None

    def __init__(self, db):
        self.db = db

    def find_by_id(self, item_id, *conditions):
        return (
            self.db.execute(select(self.table).where(self.table.c.id == item_id, *conditions))
            .mappings()
            .first()
        )

    def insert(self, values):
        result = self.db.execute(self.table.insert().values(**values))
        return result.inserted_primary_key[0]

    def update(self, item_id, values):
        values = dict(values)
        if "updated_at" in self.table.c:
            values["updated_at"] = func.now()
        self.db.execute(self.table.update().where(self.table.c.id == item_id).values(**values))

    def delete(self, item_id):
        self.db.execute(self.table.delete().where(self.table.c.id == item_id))

    def delete_where(self, *conditions):
        self.db.execute(self.table.delete().where(*conditions))

    def list_where(self, *conditions, order_by=()):
        return self.db.execute(select(self.table).where(*conditions).order_by(*order_by)).mappings().all()

    def paginate_where(self, *conditions, order_by=(), page=1, page_size=20):
        """Read a bounded page while keeping the response shape consistent across admin lists."""
        total = self.count(*conditions)
        rows = (
            self.db.execute(
                select(self.table)
                .where(*conditions)
                .order_by(*order_by)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    def count(self, *conditions):
        return self.db.scalar(select(func.count()).select_from(self.table).where(*conditions))

    def max_value(self, column, *conditions):
        return self.db.scalar(select(func.max(column)).where(*conditions))
