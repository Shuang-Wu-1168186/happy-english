"""Business rules for the study_progress table."""

from datetime import UTC, datetime, timedelta
import json
from random import sample

from fastapi import HTTPException
from sqlalchemy import case, select

from app import models as m
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
        """Build short self-review prompts from recently completed learning items."""
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
        candidates.extend(self._recent_course_review_items(user, since))
        return {"days": days, "items": sample(candidates, min(limit, len(candidates)))}

    def _recent_course_review_items(self, user, since):
        """Turn completed courseware lessons into the same prompt/answer shape.

        New course learning is stored in ``learning_progress`` rather than the
        legacy ``study_progress`` table above.  Keeping the conversion here
        lets the review page cover both learning paths without exposing a
        second client-facing review API.
        """
        from app.dao.learning_progress import LearningProgressDAO, LearningProgressItemDAO

        progress_dao = LearningProgressDAO(self.db)
        item_dao = LearningProgressItemDAO(self.db)
        candidates = []
        seen_lessons = set()
        for progress in progress_dao.list_for_user(user["id"]):
            if progress["last_studied_at"] < since:
                continue
            for item in item_dao.list_for_progress(progress["id"]):
                lesson_id = item["item_reference_id"]
                if (
                    not item["is_completed"]
                    or item["item_type"] != "material_lesson"
                    or lesson_id is None
                    or lesson_id in seen_lessons
                ):
                    continue
                if item["last_studied_at"] < since:
                    continue
                pair = self._lesson_review_pair(lesson_id)
                if pair is None:
                    continue
                prompt, answer = pair
                seen_lessons.add(lesson_id)
                candidates.append(
                    {
                        "id": item["id"],
                        "resource": "course-lessons",
                        "item_id": lesson_id,
                        "label": f"课程复习 · {progress['course_title']}",
                        "prompt": prompt,
                        "answer": answer,
                        "last_studied_at": item["last_studied_at"],
                    }
                )
        return candidates

    def _lesson_review_pair(self, lesson_id):
        """Pick one bilingual prompt from a completed, published lesson."""
        blocks = self.db.execute(
            select(m.courseware_block)
            .where(
                m.courseware_block.c.material_lesson_id == lesson_id,
                m.courseware_block.c.status == "published",
            )
            .order_by(m.courseware_block.c.sort_order, m.courseware_block.c.id)
        ).mappings()
        for block in blocks:
            try:
                payload = json.loads(block["payload_json"])
            except (TypeError, ValueError):
                continue
            sentence = payload.get("key_sentence")
            if not isinstance(sentence, dict) and block["block_type"] == "dialogue":
                sentence = next(
                    (
                        line for line in payload.get("lines", [])
                        if isinstance(line, dict) and line.get("english") and line.get("chinese")
                    ),
                    None,
                )
            if not isinstance(sentence, dict):
                continue
            prompt = str(sentence.get("english") or "").strip()
            answer = str(sentence.get("chinese") or "").strip()
            if prompt and answer:
                return prompt, answer
        return self._structured_lesson_review_pair(lesson_id)

    def _structured_lesson_review_pair(self, lesson_id):
        """Extract a dialogue line or key phrase from the generic lesson format."""
        priority = case(
            {
                "situational_dialogues": 0,
                "key_sentence_patterns": 1,
                "speaking_practice": 2,
                "core_vocabulary": 3,
            },
            value=m.learning_lesson_section.c.section_code,
            else_=10,
        )
        rows = self.db.execute(
            select(m.learning_lesson_item.c.payload_json)
            .join(
                m.learning_lesson_section,
                m.learning_lesson_item.c.section_id == m.learning_lesson_section.c.id,
            )
            .where(
                m.learning_lesson_section.c.lesson_id == lesson_id,
                m.learning_lesson_section.c.status == "published",
                m.learning_lesson_item.c.status == "published",
            )
            .order_by(priority, m.learning_lesson_item.c.item_order, m.learning_lesson_item.c.id)
        ).mappings()
        for row in rows:
            try:
                payload = json.loads(row["payload_json"])
            except (TypeError, ValueError):
                continue
            turns = payload.get("turns")
            if isinstance(turns, list):
                sentence = next(
                    (
                        turn for turn in turns
                        if isinstance(turn, dict) and turn.get("english") and turn.get("chinese")
                    ),
                    None,
                )
                if sentence:
                    return sentence["english"].strip(), sentence["chinese"].strip()
            for prompt_key, answer_key in (
                ("pattern", "meaning"),
                ("term", "meaning"),
                ("english", "chinese"),
            ):
                prompt = str(payload.get(prompt_key) or "").strip()
                answer = str(payload.get(answer_key) or "").strip()
                if prompt and answer:
                    return prompt, answer
        return None

    def save(self, user, data):
        # Import lazily so ContentService can use this service for delete cascades.
        from app.services.content import ContentService
        from app.services.membership import MembershipService

        content = ContentService(self.db)
        if data.content_type == "english_note":
            # The learning page is also available to administrators, who can
            # preview unpublished platform cards.  Pass the current user
            # through so content visibility stays consistent with the list
            # endpoint instead of treating those cards as missing.
            item = content.get_content("note-items", data.item_id, user)
            content.get_content("notes", data.parent_id, user)
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
