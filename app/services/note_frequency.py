"""Business operations for manually tracking note vocabulary encounters."""

from app import models as m
from app.dao.note_frequency import NoteItemFrequencyDAO


class NoteItemFrequencyService:
    def __init__(self, db):
        self.dao = NoteItemFrequencyDAO(db)

    def count_for_item(self, user_id, item_id):
        return self.dao.count_for_user(user_id, item_id)

    def counts_for_items(self, user_id, item_ids):
        return self.dao.counts_for_user(user_id, item_ids)

    def increment(self, user_id, item_id):
        return self.dao.increment(user_id, item_id)


NOTE_ITEM_FREQUENCY_TABLE_SERVICE_TYPES = {
    m.english_note_item_frequency.name: NoteItemFrequencyService,
}
