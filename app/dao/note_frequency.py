"""Persistence for each user's manual note-item encounter count."""

from sqlalchemy import func, select

from app import models as m


class NoteItemFrequencyDAO:
    table = m.english_note_item_frequency

    def counts_for_user(self, user_id, item_ids):
        item_ids = list(dict.fromkeys(item_ids))
        if not item_ids:
            return {}
        rows = self.db.execute(
            select(self.table.c.note_item_id, self.table.c.frequency_count).where(
                self.table.c.user_id == user_id,
                self.table.c.note_item_id.in_(item_ids),
            )
        ).all()
        return {int(item_id): int(count) for item_id, count in rows}

    def __init__(self, db):
        self.db = db

    def count_for_user(self, user_id, item_id):
        return self.counts_for_user(user_id, [item_id]).get(item_id, 0)

    def increment(self, user_id, item_id):
        values = {
            "user_id": user_id,
            "note_item_id": item_id,
            "frequency_count": 1,
            "last_recorded_at": func.now(),
            "updated_at": func.now(),
        }
        dialect = self.db.get_bind().dialect.name
        if dialect == "mysql":
            from sqlalchemy.dialects.mysql import insert

            statement = insert(self.table).values(**values).on_duplicate_key_update(
                frequency_count=self.table.c.frequency_count + 1,
                last_recorded_at=func.now(),
                updated_at=func.now(),
            )
        else:
            from sqlalchemy.dialects.sqlite import insert

            statement = insert(self.table).values(**values).on_conflict_do_update(
                index_elements=["user_id", "note_item_id"],
                set_={
                    "frequency_count": self.table.c.frequency_count + 1,
                    "last_recorded_at": func.now(),
                    "updated_at": func.now(),
                },
            )
        self.db.execute(statement)
        return self.count_for_user(user_id, item_id)


NOTE_ITEM_FREQUENCY_TABLE_DAO_TYPES = {
    m.english_note_item_frequency.name: NoteItemFrequencyDAO,
}
