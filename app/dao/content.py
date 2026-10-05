"""Table-specific DAOs for all learning-content tables."""

from sqlalchemy import String, Text, func, or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class ContentTableDAO(BaseTableDAO):
    """Common reads and writes for a single learning-content table."""

    resource = None

    def visible_conditions(self):
        for name in ("is_active", "is_published", "status"):
            if name in self.table.c:
                return [self.table.c[name] == 1]
        return []

    def ordering(self):
        if self.table is m.english_note:
            return [self.table.c.note_date.desc(), self.table.c.id.desc()]
        return [
            self.table.c[name]
            for name in (
                "priority_order",
                "sort_order",
                "unit_order",
                "lesson_order",
                "section_order",
                "part_order",
                "sentence_order",
                "item_order",
            )
            if name in self.table.c
        ] + [self.table.c.id]

    def list_ordering(self):
        """Content library search results are management lists, not lesson flow."""
        return self.newest_first_ordering()

    def text_matches(self, query):
        return or_(
            *(
                column.ilike(f"%{query}%")
                for column in self.table.c
                if isinstance(column.type, (String, Text))
            )
        )

    def related_search_condition(self, query):
        return None

    def list_content(
        self,
        q="",
        category="",
        parent_id=None,
        page=1,
        page_size=20,
        language_register="",
        scenario="",
    ):
        conditions = self.visible_conditions()
        q = q.strip()
        if q:
            matches = self.text_matches(q)
            related = self.related_search_condition(q)
            if related is not None:
                matches = or_(matches, related)
            conditions.append(matches)
        if category:
            field = next(
                (
                    name
                    for name in (
                        "category",
                        "tag",
                        "category_id",
                        "unit_name",
                        "lesson_code",
                    )
                    if name in self.table.c
                ),
                None,
            )
            if field:
                conditions.append(self.table.c[field] == category)
        if parent_id is not None and "note_id" in self.table.c:
            conditions.append(self.table.c.note_id == parent_id)
        if language_register and "language_register" in self.table.c:
            conditions.append(self.table.c.language_register == language_register)
        if scenario and "usage_scenarios_json" in self.table.c:
            conditions.append(self.table.c.usage_scenarios_json.ilike(f'%"{scenario}"%'))
        total = self.count(*conditions)
        rows = (
            self.db.execute(
                select(self.table)
                .where(*conditions)
                .order_by(*self.list_ordering())
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

    def get_published(self, item_id):
        return self.find_by_id(item_id, *self.visible_conditions())

    def neighbor_ids(self, item_id, parent_id=None):
        conditions = self.visible_conditions()
        if parent_id is not None and "note_id" in self.table.c:
            conditions.append(self.table.c.note_id == parent_id)
        navigation = (
            select(
                self.table.c.id,
                func.lag(self.table.c.id).over(order_by=self.ordering()).label("previous_id"),
                func.lead(self.table.c.id).over(order_by=self.ordering()).label("next_id"),
            )
            .where(*conditions)
            .subquery()
        )
        return self.db.execute(select(navigation).where(navigation.c.id == item_id)).mappings().one_or_none()

    def list_for_parent(self, foreign_key, parent_id):
        if foreign_key not in self.table.c:
            return []
        return self.list_where(
            self.table.c[foreign_key] == parent_id,
            *self.visible_conditions(),
            order_by=self.ordering(),
        )

    def next_order(self, column_name, value):
        return (self.max_value(self.table.c.item_order, self.table.c[column_name] == value) or 0) + 1


class EnglishNoteDAO(ContentTableDAO):
    resource = "notes"
    table = m.english_note

    def related_search_condition(self, query):
        items = EnglishNoteItemDAO(self.db)
        return (
            select(items.table.c.id)
            .where(
                items.table.c.note_id == self.table.c.id,
                items.text_matches(query),
                *items.visible_conditions(),
            )
            .exists()
        )


class EnglishNoteItemDAO(ContentTableDAO):
    resource = "note-items"
    table = m.english_note_item

    def related_search_condition(self, query):
        notes = EnglishNoteDAO(self.db)
        return (
            select(notes.table.c.id)
            .where(
                notes.table.c.id == self.table.c.note_id,
                notes.text_matches(query),
                *notes.visible_conditions(),
            )
            .exists()
        )


class EverydaySentenceDAO(ContentTableDAO):
    resource = "sentences"
    table = m.everyday_sentence


class InterviewAnswerSectionDAO(ContentTableDAO):
    table = m.interview_answer_section


class InterviewCategoryDAO(ContentTableDAO):
    resource = "interview-categories"
    table = m.interview_category


class InterviewQuestionDAO(ContentTableDAO):
    resource = "interviews"
    table = m.interview_question


class InterviewQuestionTagDAO(ContentTableDAO):
    table = m.interview_question_tag


class KidsEnglishCardDAO(ContentTableDAO):
    resource = "kids-cards"
    table = m.kids_english_card


class KidsEnglishCardExampleDAO(ContentTableDAO):
    table = m.kids_english_card_example


class KidsEnglishCardSoundPartDAO(ContentTableDAO):
    table = m.kids_english_card_sound_part


class KidsEnglishCardWordFamilyDAO(ContentTableDAO):
    table = m.kids_english_card_word_family


class VocabularyLibraryDAO(ContentTableDAO):
    resource = "vocabulary"
    table = m.vocabulary_library


class MathCardDAO(ContentTableDAO):
    resource = "math-cards"
    table = m.math_card


class EnglishTextbookLessonDAO(ContentTableDAO):
    resource = "textbook"
    table = m.english_textbook_lesson


class EnglishTextbookSentenceDAO(ContentTableDAO):
    table = m.english_textbook_sentence


class PhonicsLessonDAO(ContentTableDAO):
    resource = "phonics"
    table = m.phonics_lesson


CONTENT_TABLE_DAO_TYPES = {
    m.english_note.name: EnglishNoteDAO,
    m.english_note_item.name: EnglishNoteItemDAO,
    m.everyday_sentence.name: EverydaySentenceDAO,
    m.interview_answer_section.name: InterviewAnswerSectionDAO,
    m.interview_category.name: InterviewCategoryDAO,
    m.interview_question.name: InterviewQuestionDAO,
    m.interview_question_tag.name: InterviewQuestionTagDAO,
    m.kids_english_card.name: KidsEnglishCardDAO,
    m.kids_english_card_example.name: KidsEnglishCardExampleDAO,
    m.kids_english_card_sound_part.name: KidsEnglishCardSoundPartDAO,
    m.kids_english_card_word_family.name: KidsEnglishCardWordFamilyDAO,
    m.vocabulary_library.name: VocabularyLibraryDAO,
    m.math_card.name: MathCardDAO,
    m.english_textbook_lesson.name: EnglishTextbookLessonDAO,
    m.english_textbook_sentence.name: EnglishTextbookSentenceDAO,
    m.phonics_lesson.name: PhonicsLessonDAO,
}

RESOURCE_DAO_TYPES = {
    dao_type.resource: dao_type for dao_type in CONTENT_TABLE_DAO_TYPES.values() if dao_type.resource
}
