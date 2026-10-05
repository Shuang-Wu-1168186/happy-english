"""Learning-content services: validation and aggregate business rules."""

import json

from fastapi import HTTPException
from pydantic import ValidationError

from app import schemas as s
from app.dao.content import (
    EnglishNoteDAO,
    EnglishNoteItemDAO,
    EnglishTextbookLessonDAO,
    EnglishTextbookSentenceDAO,
    EverydaySentenceDAO,
    InterviewAnswerSectionDAO,
    InterviewCategoryDAO,
    InterviewQuestionDAO,
    InterviewQuestionTagDAO,
    KidsEnglishCardDAO,
    KidsEnglishCardExampleDAO,
    KidsEnglishCardSoundPartDAO,
    KidsEnglishCardWordFamilyDAO,
    MathCardDAO,
    PhonicsLessonDAO,
    VocabularyLibraryDAO,
)
from app.services.note_language import classify_note_item


INPUT_SCHEMAS = {
    "sentences": s.SentenceInput,
    "notes": s.NoteInput,
    "note-items": s.NoteItemInput,
    "vocabulary": s.VocabularyInput,
    "interviews": s.InterviewInput,
}


def serialise_content(row):
    """Expose JSON-backed columns as values while leaving database rows immutable."""
    result = dict(row)
    for key, value in list(result.items()):
        if not key.endswith("_json"):
            continue
        if isinstance(value, str):
            try:
                value = json.loads(value or "[]")
            except (TypeError, ValueError):
                value = []
        elif value is None:
            value = []
        result[key.removesuffix("_json")] = value
    return result


class ContentTableService:
    """Generic service for one content table; subclasses declare its DAO."""

    dao_type = None

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def list(
        self,
        q="",
        category="",
        parent_id=None,
        page=1,
        page_size=20,
        language_register="",
        scenario="",
    ):
        result = self.dao.list_content(
            q,
            category,
            parent_id,
            page,
            page_size,
            language_register,
            scenario,
        )
        return {**result, "items": [serialise_content(row) for row in result["items"]]}

    def require(self, item_id):
        row = self.dao.get_published(item_id)
        if not row:
            raise HTTPException(404, "Content not found.")
        return row

    def delete_for(self, foreign_key, parent_id):
        self.dao.delete_where(self.dao.table.c[foreign_key] == parent_id)


class EnglishNoteService(ContentTableService):
    dao_type = EnglishNoteDAO


class EnglishNoteItemService(ContentTableService):
    dao_type = EnglishNoteItemDAO


class EverydaySentenceService(ContentTableService):
    dao_type = EverydaySentenceDAO


class InterviewAnswerSectionService(ContentTableService):
    dao_type = InterviewAnswerSectionDAO

    def replace_for_question(self, question_id, sections, created_by):
        self.delete_for("question_id", question_id)
        for order, section in enumerate(sections):
            self.dao.insert(
                {
                    **section,
                    "question_id": question_id,
                    "sort_order": order,
                    "created_by": created_by,
                }
            )


class InterviewCategoryService(ContentTableService):
    dao_type = InterviewCategoryDAO


class InterviewQuestionService(ContentTableService):
    dao_type = InterviewQuestionDAO


class InterviewQuestionTagService(ContentTableService):
    dao_type = InterviewQuestionTagDAO


class KidsEnglishCardService(ContentTableService):
    dao_type = KidsEnglishCardDAO


class KidsEnglishCardExampleService(ContentTableService):
    dao_type = KidsEnglishCardExampleDAO


class KidsEnglishCardSoundPartService(ContentTableService):
    dao_type = KidsEnglishCardSoundPartDAO


class KidsEnglishCardWordFamilyService(ContentTableService):
    dao_type = KidsEnglishCardWordFamilyDAO


class VocabularyLibraryService(ContentTableService):
    dao_type = VocabularyLibraryDAO


class MathCardService(ContentTableService):
    dao_type = MathCardDAO


class EnglishTextbookLessonService(ContentTableService):
    dao_type = EnglishTextbookLessonDAO


class EnglishTextbookSentenceService(ContentTableService):
    dao_type = EnglishTextbookSentenceDAO


class PhonicsLessonService(ContentTableService):
    dao_type = PhonicsLessonDAO


CONTENT_TABLE_SERVICE_TYPES = {
    "english_note": EnglishNoteService,
    "english_note_item": EnglishNoteItemService,
    "everyday_sentence": EverydaySentenceService,
    "interview_answer_section": InterviewAnswerSectionService,
    "interview_category": InterviewCategoryService,
    "interview_question": InterviewQuestionService,
    "interview_question_tag": InterviewQuestionTagService,
    "kids_english_card": KidsEnglishCardService,
    "kids_english_card_example": KidsEnglishCardExampleService,
    "kids_english_card_sound_part": KidsEnglishCardSoundPartService,
    "kids_english_card_word_family": KidsEnglishCardWordFamilyService,
    "vocabulary_library": VocabularyLibraryService,
    "math_card": MathCardService,
    "english_textbook_lesson": EnglishTextbookLessonService,
    "english_textbook_sentence": EnglishTextbookSentenceService,
    "phonics_lesson": PhonicsLessonService,
}

RESOURCE_SERVICE_TYPES = {
    "sentences": EverydaySentenceService,
    "notes": EnglishNoteService,
    "note-items": EnglishNoteItemService,
    "vocabulary": VocabularyLibraryService,
    "interviews": InterviewQuestionService,
    "interview-categories": InterviewCategoryService,
    "kids-cards": KidsEnglishCardService,
    "math-cards": MathCardService,
    "textbook": EnglishTextbookLessonService,
    "phonics": PhonicsLessonService,
}

CHILDREN = {
    "kids-cards": [
        ("examples", "kids_english_card_example", "card_id"),
        ("sound_parts", "kids_english_card_sound_part", "card_id"),
        ("word_family", "kids_english_card_word_family", "card_id"),
    ],
    "interviews": [("sections", "interview_answer_section", "question_id")],
    "textbook": [("sentences", "english_textbook_sentence", "lesson_id")],
    "notes": [("items", "english_note_item", "note_id")],
}


class ContentService:
    """Application service used by the content API controller."""

    def __init__(self, db):
        self.db = db

    def resource_service(self, resource):
        service_type = RESOURCE_SERVICE_TYPES.get(resource)
        if not service_type:
            raise HTTPException(404, "Unknown learning module.")
        return service_type(self.db)

    def table_service(self, table_name):
        return CONTENT_TABLE_SERVICE_TYPES[table_name](self.db)

    def module_counts(self):
        counts = {}
        for resource, service_type in RESOURCE_SERVICE_TYPES.items():
            service = service_type(self.db)
            counts[resource] = service.dao.count(*service.dao.visible_conditions())
        return counts

    def list_content(
        self,
        resource,
        q="",
        category="",
        parent_id=None,
        page=1,
        page_size=20,
        language_register="",
        scenario="",
    ):
        return self.resource_service(resource).list(
            q,
            category,
            parent_id,
            page,
            page_size,
            language_register,
            scenario,
        )

    def get_content(self, resource, item_id):
        service = self.resource_service(resource)
        row = service.require(item_id)
        result = serialise_content(row)
        parent_id = row.get("note_id") if resource == "note-items" else None
        neighbors = service.dao.neighbor_ids(item_id, parent_id)
        if neighbors:
            result.update(
                previous_id=neighbors["previous_id"],
                next_id=neighbors["next_id"],
            )
        else:
            result.update(previous_id=None, next_id=None)
        for key, table_name, foreign_key in CHILDREN.get(resource, []):
            child_service = self.table_service(table_name)
            rows = child_service.dao.list_for_parent(foreign_key, item_id)
            result[key] = [serialise_content(child) for child in rows]
        return result

    def save(self, resource, payload, admin, item_id=None):
        schema = INPUT_SCHEMAS.get(resource)
        if not schema:
            raise HTTPException(405, "This module is maintained through SQL imports.")
        try:
            values = schema.model_validate(payload).model_dump()
        except ValidationError as error:
            raise HTTPException(422, error.errors(include_context=False)) from error

        sections = values.pop("sections", None)
        service = self.resource_service(resource)
        classification_fields = None
        manual_classification = False
        if resource == "note-items":
            language_register = values.pop("language_register", None)
            usage_scenarios = values.pop("usage_scenarios", None)
            register_reason = values.pop("register_reason", None)
            manual_classification = any(
                value is not None for value in (language_register, usage_scenarios, register_reason)
            )
            if manual_classification:
                classification_fields = {
                    "language_register": language_register or "unclassified",
                    "usage_scenarios_json": json.dumps(usage_scenarios or [], ensure_ascii=False),
                    "register_reason": register_reason or "",
                    "classification_confidence": 100,
                    "classification_source": "manual",
                }
        if resource == "note-items":
            self.resource_service("notes").require(values["note_id"])
        if resource == "interviews":
            self.resource_service("interview-categories").require(values["category_id"])

        if item_id is None:
            if resource == "note-items":
                values["item_order"] = service.dao.next_order("note_id", values["note_id"])
                if not manual_classification:
                    classification = classify_note_item(values)
                    classification_fields = {
                        "language_register": classification.language_register,
                        "usage_scenarios_json": json.dumps(
                            classification.usage_scenarios, ensure_ascii=False
                        ),
                        "register_reason": classification.register_reason,
                        "classification_confidence": classification.classification_confidence,
                        "classification_source": classification.classification_source,
                    }
                values.update(classification_fields or {})
            if "created_by" in service.dao.table.c:
                values["created_by"] = admin["id"]
            item_id = service.dao.insert(values)
        else:
            current = service.require(item_id)
            if resource == "note-items" and manual_classification:
                try:
                    current_scenarios = json.loads(current.get("usage_scenarios_json") or "[]")
                except (TypeError, ValueError):
                    current_scenarios = []
                if (
                    current.get("classification_source") != "manual"
                    and classification_fields["language_register"] == current.get("language_register")
                    and json.loads(classification_fields["usage_scenarios_json"]) == current_scenarios
                    and classification_fields["register_reason"] == (current.get("register_reason") or "")
                ):
                    manual_classification = False
                    classification_fields = None
            if resource == "note-items" and not manual_classification:
                if current.get("classification_source") != "manual":
                    classification = classify_note_item(values)
                    classification_fields = {
                        "language_register": classification.language_register,
                        "usage_scenarios_json": json.dumps(
                            classification.usage_scenarios, ensure_ascii=False
                        ),
                        "register_reason": classification.register_reason,
                        "classification_confidence": classification.classification_confidence,
                        "classification_source": classification.classification_source,
                    }
            values.update(classification_fields or {})
            if "updated_by" in service.dao.table.c:
                values["updated_by"] = admin["id"]
            service.dao.update(item_id, values)

        if sections is not None:
            self.table_service("interview_answer_section").replace_for_question(
                item_id,
                sections,
                admin["id"],
            )
        self.db.commit()
        return self.get_content(resource, item_id)

    def delete(self, resource, item_id):
        if resource not in INPUT_SCHEMAS:
            raise HTTPException(405, "This module is maintained through SQL imports.")
        self.resource_service(resource).require(item_id)

        from app.services.progress import StudyProgressService

        progress = StudyProgressService(self.db)
        if resource == "notes":
            progress.delete_for_parent("english_note", item_id)
            self.table_service("english_note_item").delete_for("note_id", item_id)
        if resource in {"sentences", "note-items"}:
            progress.delete_for_item(
                "everyday_sentence" if resource == "sentences" else "english_note",
                item_id,
            )
        if resource == "interviews":
            self.table_service("interview_answer_section").delete_for("question_id", item_id)
            self.table_service("interview_question_tag").delete_for("question_id", item_id)
        self.resource_service(resource).dao.delete(item_id)
        self.db.commit()
