"""Business rules for the study_progress table."""

from datetime import UTC, datetime, timedelta
from random import sample

from fastapi import HTTPException

from app.dao.progress import StudyProgressDAO


class StudyProgressService:
    """Service corresponding to the study_progress table."""

    def __init__(self, db):
        self.db = db
        self.dao = StudyProgressDAO(db)

    def list_for_user(self, user_id):
        return self.dao.list_for_user(user_id)

    @staticmethod
    def _first_text(item, *fields):
        for field in fields:
            value = item.get(field)
            if value is not None and str(value).strip():
                return str(value).strip()
        return ""

    def recent_review_items(self, user, days=7, limit=3):
        """Build short self-review prompts from recent legacy study records."""
        from app.services.content import ContentService
        from app.services.membership import MembershipService

        since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)
        content = ContentService(self.db)
        legacy_sentence_access = MembershipService(self.db).can_open_legacy_content(user, "sentences")
        candidates = []
        for record in self.dao.list_recent_for_user(user["id"], since):
            if record["content_type"] == "everyday_sentence":
                if not legacy_sentence_access:
                    continue
                resource, label = "sentences", "日常短语"
                prompt_fields = ("en", "english_text")
                answer_fields = ("cn", "chinese_text", "note")
            elif record["content_type"] == "english_note":
                resource, label = "note-items", "学习卡片"
                prompt_fields = ("english_text", "raw_text", "item_title")
                answer_fields = ("chinese_text", "explanation", "item_title")
            else:
                continue
            try:
                item = content.get_content(resource, record["item_id"])
            except HTTPException:
                continue
            prompt = self._first_text(item, *prompt_fields)
            answer = self._first_text(item, *answer_fields)
            if not prompt or not answer:
                continue
            candidates.append(
                {
                    "id": record["id"],
                    "resource": resource,
                    "item_id": item["id"],
                    "label": label,
                    "prompt": prompt,
                    "answer": answer,
                    "last_studied_at": record["last_studied_at"],
                }
            )
        return {"days": days, "items": sample(candidates, min(limit, len(candidates)))}

    def save(self, user, data):
        # Import lazily so ContentService can use this service for delete cascades.
        from app.services.content import ContentService
        from app.services.membership import MembershipService

        content = ContentService(self.db)
        if data.content_type == "english_note":
            item = content.get_content("note-items", data.item_id)
            content.get_content("notes", data.parent_id)
            if item["note_id"] != data.parent_id:
                raise HTTPException(400, "This card does not belong to the selected note.")
        else:
            MembershipService(self.db).require_legacy_content_access(user, "sentences")
            content.get_content("sentences", data.item_id)
            data.parent_id = 0
        values = data.model_dump()
        values.update(user_id=user["id"], completed=int(data.completed))
        self.dao.save(values)
        self.db.commit()
        return {"success": True}

    def delete_for_parent(self, content_type, parent_id):
        self.dao.delete_for_parent(content_type, parent_id)

    def delete_for_item(self, content_type, item_id):
        self.dao.delete_for_item(content_type, item_id)
