"""Active-recall review sessions built from the learner's studied content."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from random import shuffle
import re
import unicodedata

from fastapi import HTTPException
from sqlalchemy import func, select

from app import models as m
from app import schemas as s
from app.dao.learning_progress import LearningProgressDAO, LearningProgressItemDAO
from app.dao.progress import StudyProgressDAO
from app.dao.review import LearningReviewQuestionDAO, LearningReviewSessionDAO
from app.services.content import ContentService
from app.services.courseware import NoteCoursewareService
from app.services.learning_progress import LearningProgressService
from app.services.membership import MembershipService, REVIEW_AI_BENEFIT_CODE
from app.services.review_ai import ReviewCandidate, ReviewQuestionPlan


REVIEW_SOURCE_NOTES = "notes"
REVIEW_SOURCE_TEXTBOOKS = "textbooks"
REVIEW_SOURCE_TYPES = (REVIEW_SOURCE_NOTES, REVIEW_SOURCE_TEXTBOOKS)


def normalize_review_answer(value: str) -> str:
    """Compare English answers without penalising casing or punctuation."""

    normalized = unicodedata.normalize("NFKC", value or "")
    normalized = normalized.replace("’", "'").replace("‘", "'").replace("`", "'")
    return re.sub(r"[^\w]+", "", normalized, flags=re.UNICODE).casefold()


class LearningReviewSessionService:
    """Build, persist, and grade one learner's sentence-based review round."""

    session_dao_type = LearningReviewSessionDAO
    question_dao_type = LearningReviewQuestionDAO

    def __init__(self, db, question_generator=None):
        self.db = db
        self.sessions = self.session_dao_type(db)
        self.questions = self.question_dao_type(db)
        self.question_generator = question_generator

    def create(self, user, data: s.LearningReviewSessionInput):
        since = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=data.days)
        source_types = list(data.source_types)
        candidates = self._deduplicate(
            self._recent_candidates(user, since, source_types)
        )
        selected, provider, model = self._select_questions(
            candidates,
            data.limit,
            use_ai=self._can_use_ai_generation(user),
        )
        session_id = self.sessions.insert(
            {
                "user_id": user["id"],
                "source_window_days": data.days,
                "source_types_json": json.dumps(
                    source_types,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                "generator_provider": provider,
                "generator_model": model,
                "question_count": len(selected),
            }
        )
        for order, (candidate, plan) in enumerate(selected, start=1):
            accepted_answers = self._merge_accepted_answers(
                candidate.english,
                plan.accepted_answers,
            )
            self.questions.insert(
                {
                    "session_id": session_id,
                    "source_type": candidate.source_type,
                    "source_id": candidate.source_id,
                    "source_parent_id": candidate.source_parent_id,
                    "source_label": candidate.source_label,
                    "source_locator": candidate.source_locator or None,
                    "question_type": "translate_to_english",
                    "answer_mode": "normalized_exact",
                    "prompt": candidate.chinese,
                    "context_text": "",
                    "reference_answer": candidate.english,
                    "accepted_answers_json": json.dumps(
                        accepted_answers,
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    "explanation": (plan.explanation or candidate.explanation) or None,
                    "question_order": order,
                }
            )
        self.db.commit()
        return self.get(user, session_id)

    def get(self, user, session_id):
        session = self.sessions.get_for_user(session_id, user["id"])
        if not session:
            raise HTTPException(404, "Review session not found.")
        questions = self.questions.list_for_session(session_id)
        return {
            "id": session["id"],
            "days": session["source_window_days"],
            "source_types": self._session_source_types(session),
            "generation": {
                "provider": session["generator_provider"] or "deterministic",
                "model": session["generator_model"] or "",
                "fallback": session["generator_provider"] != "deepseek",
            },
            "created_at": session["created_at"],
            "completed_at": session["completed_at"],
            "summary": self._summary(session, questions),
            "questions": [self._question_view(question) for question in questions],
        }

    def submit_answer(self, user, session_id, data: s.LearningReviewAnswerInput):
        session = self.sessions.get_for_user(session_id, user["id"])
        if not session:
            raise HTTPException(404, "Review session not found.")
        question = self.questions.get_for_session(data.question_id, session_id)
        if not question:
            raise HTTPException(404, "Review question not found.")
        if question["answered_at"] is not None:
            return self._answer_view(session, question, already_answered=True)

        expected = self._accepted_answers(question)
        answer = data.answer.strip()
        is_correct = any(
            normalize_review_answer(answer) == normalize_review_answer(value)
            for value in expected
        )
        self.questions.update(
            question["id"],
            {
                "attempt_count": int(question["attempt_count"] or 0) + 1,
                "submitted_answer": answer,
                "is_correct": int(is_correct),
                "answered_at": func.now(),
            },
        )
        if self.questions.count_answered(session_id) >= int(session["question_count"] or 0):
            self.sessions.mark_completed(session_id)
        self.db.commit()
        refreshed_session = self.sessions.get_for_user(session_id, user["id"])
        refreshed_question = self.questions.get_for_session(data.question_id, session_id)
        return self._answer_view(refreshed_session, refreshed_question, already_answered=False)

    def _can_use_ai_generation(self, user):
        return MembershipService(self.db).has_feature_access(
            user,
            REVIEW_AI_BENEFIT_CODE,
        )

    def _select_questions(self, candidates, limit, *, use_ai=False):
        if not candidates:
            return [], "deterministic", ""

        if use_ai and self.question_generator is not None:
            selection = self.question_generator.generate(candidates, limit)
            if selection and selection.plans:
                selected = []
                selected_ids = set()
                for plan in selection.plans:
                    if (
                        plan.candidate_id < 0
                        or plan.candidate_id >= len(candidates)
                        or plan.candidate_id in selected_ids
                    ):
                        continue
                    selected_ids.add(plan.candidate_id)
                    selected.append((candidates[plan.candidate_id], plan))
                    if len(selected) >= limit:
                        break
                if selected:
                    remaining = [
                        candidate
                        for candidate_id, candidate in enumerate(candidates)
                        if candidate_id not in selected_ids
                    ]
                    for candidate in self._balanced_sample(
                        remaining,
                        min(limit - len(selected), len(remaining)),
                    ):
                        selected.append((candidate, ReviewQuestionPlan(candidate_id=-1)))
                    return selected, selection.provider, selection.model

        selected = [
            (candidate, ReviewQuestionPlan(candidate_id=-1))
            for candidate in self._balanced_sample(
                candidates,
                min(limit, len(candidates)),
            )
        ]
        return selected, "deterministic", ""

    @staticmethod
    def _balanced_sample(candidates, limit):
        if limit <= 0:
            return []
        grouped = {}
        for candidate in candidates:
            grouped.setdefault(candidate.source_type, []).append(candidate)
        for group in grouped.values():
            shuffle(group)

        result = []
        groups = list(grouped.values())
        offset = 0
        while len(result) < limit:
            added = False
            for group in groups:
                if offset < len(group) and len(result) < limit:
                    result.append(group[offset])
                    added = True
            if not added:
                break
            offset += 1
        return result

    @classmethod
    def _merge_accepted_answers(cls, reference_answer, generated_answers):
        result = []
        seen = set()
        for value in (reference_answer, *generated_answers):
            value = cls._clean(value)
            normalized = normalize_review_answer(value)
            if value and normalized and normalized not in seen:
                seen.add(normalized)
                result.append(value)
            if len(result) >= 6:
                break
        return result or [reference_answer]

    @staticmethod
    def _session_source_types(session):
        try:
            decoded = json.loads(session["source_types_json"])
        except (TypeError, ValueError):
            decoded = []
        values = [
            value
            for value in decoded
            if isinstance(value, str) and value in REVIEW_SOURCE_TYPES
        ]
        return values or list(REVIEW_SOURCE_TYPES)

    def _recent_candidates(self, user, since, source_types):
        candidates = []
        if REVIEW_SOURCE_NOTES in source_types:
            candidates.extend(self._note_candidates(user, since))
        if REVIEW_SOURCE_TEXTBOOKS in source_types:
            candidates.extend(self._course_candidates(user, since))
        return candidates

    def _note_candidates(self, user, since):
        content = ContentService(self.db)
        progress = StudyProgressDAO(self.db)
        candidates = []
        for record in progress.list_recent_for_user(user["id"], since):
            if record["content_type"] != "english_note":
                continue
            try:
                item = content.get_content("note-items", record["item_id"], user)
            except HTTPException:
                continue

            note = self.db.execute(
                select(m.english_note.c.title).where(m.english_note.c.id == record["parent_id"])
            ).mappings().first()
            note_title = self._clean(note["title"] if note else "") or "英语笔记"
            label = f"英语笔记 · {note_title}"
            pairs = []
            # Examples come first: a note card's headline is useful context,
            # but practice should favour sentences learners can actually use.
            for field in ("examples", "explanation", "raw_text"):
                pairs.extend(NoteCoursewareService._pairs(item.get(field) or ""))
            pairs.append((item.get("english_text") or "", item.get("chinese_text") or ""))
            for index, pair in enumerate(pairs, start=1):
                if isinstance(pair, dict):
                    english, chinese = pair.get("english", ""), pair.get("chinese", "")
                else:
                    english, chinese = pair
                candidate = self._candidate(
                    source_type="english_note_item",
                    source_id=item["id"],
                    source_parent_id=record["parent_id"],
                    source_label=label,
                    source_locator=f"example-{index}",
                    english=english,
                    chinese=chinese,
                    explanation=item.get("explanation"),
                )
                if candidate:
                    candidates.append(candidate)
        return candidates

    def _course_candidates(self, user, since):
        progress_dao = LearningProgressDAO(self.db)
        item_dao = LearningProgressItemDAO(self.db)
        course_access = LearningProgressService(self.db)
        candidates = []
        checked_courses = set()
        blocked_courses = set()
        seen_lessons = set()
        for progress in progress_dao.list_for_user(user["id"]):
            if progress["last_studied_at"] < since:
                continue
            course_id = progress["course_id"]
            if course_id not in checked_courses and course_id not in blocked_courses:
                try:
                    course_access.require_course(course_id, user)
                    checked_courses.add(course_id)
                except HTTPException:
                    blocked_courses.add(course_id)
            if course_id in blocked_courses:
                continue

            for item in item_dao.list_for_progress(progress["id"]):
                lesson_id = item["item_reference_id"]
                if (
                    not item["is_completed"]
                    or item["item_type"] != "material_lesson"
                    or lesson_id is None
                    or lesson_id in seen_lessons
                    or item["last_studied_at"] < since
                ):
                    continue
                lesson = self.db.execute(
                    select(m.learning_material_lesson).where(
                        m.learning_material_lesson.c.id == lesson_id,
                        m.learning_material_lesson.c.is_published == 1,
                    )
                ).mappings().first()
                if not lesson:
                    continue
                seen_lessons.add(lesson_id)
                label = f"教材例句 · {self._clean(progress['course_title']) or lesson['title']}"
                for index, (english, chinese) in enumerate(self._lesson_pairs(lesson, user), start=1):
                    candidate = self._candidate(
                        source_type="material_lesson",
                        source_id=lesson_id,
                        source_parent_id=course_id,
                        source_label=label,
                        source_locator=f"sentence-{index}",
                        english=english,
                        chinese=chinese,
                        explanation=lesson.get("summary"),
                    )
                    if candidate:
                        candidates.append(candidate)
        return candidates

    def _lesson_pairs(self, lesson, user):
        pairs = []
        content_json = lesson.get("content_json")
        if content_json:
            try:
                pairs.extend(self._payload_pairs(json.loads(content_json)))
            except (TypeError, ValueError):
                pass

        resource = lesson.get("source_resource")
        reference_id = lesson.get("source_reference_id")
        if resource and reference_id:
            try:
                source = ContentService(self.db).get_content(resource, reference_id, user)
                pairs.extend(self._payload_pairs(source))
            except HTTPException:
                pass

        blocks = self.db.execute(
            select(m.courseware_block.c.payload_json)
            .where(
                m.courseware_block.c.material_lesson_id == lesson["id"],
                m.courseware_block.c.status == "published",
            )
            .order_by(m.courseware_block.c.sort_order, m.courseware_block.c.id)
        ).mappings()
        for block in blocks:
            try:
                pairs.extend(self._payload_pairs(json.loads(block["payload_json"])))
            except (TypeError, ValueError):
                continue

        sections = self.db.execute(
            select(m.learning_lesson_item.c.payload_json)
            .join(
                m.learning_lesson_section,
                m.learning_lesson_item.c.section_id == m.learning_lesson_section.c.id,
            )
            .where(
                m.learning_lesson_section.c.lesson_id == lesson["id"],
                m.learning_lesson_section.c.status == "published",
                m.learning_lesson_item.c.status == "published",
            )
            .order_by(
                m.learning_lesson_section.c.sort_order,
                m.learning_lesson_item.c.item_order,
                m.learning_lesson_item.c.id,
            )
        ).mappings()
        for row in sections:
            try:
                pairs.extend(self._payload_pairs(json.loads(row["payload_json"])))
            except (TypeError, ValueError):
                continue
        return pairs

    @classmethod
    def _payload_pairs(cls, payload):
        pairs = []
        pair_fields = (
            ("english", "chinese"),
            ("english_text", "chinese_text"),
            ("en", "cn"),
            ("example_text", "translation"),
            ("phrase", "meaning"),
            ("pattern", "meaning"),
        )

        def visit(value):
            if isinstance(value, dict):
                for english_key, chinese_key in pair_fields:
                    english = value.get(english_key)
                    chinese = value.get(chinese_key)
                    if isinstance(english, str) and isinstance(chinese, str):
                        pairs.append((english, chinese))
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(payload)
        return pairs

    @classmethod
    def _candidate(
        cls,
        *,
        source_type,
        source_id,
        source_parent_id,
        source_label,
        source_locator,
        english,
        chinese,
        explanation,
    ):
        english = cls._clean(english)
        chinese = cls._clean(chinese)
        if (
            not english
            or not chinese
            or not re.search(r"[A-Za-z]", english)
            or not re.search(r"[\u4e00-\u9fff]", chinese)
            or len(english) > 500
            or len(chinese) > 500
        ):
            return None
        return ReviewCandidate(
            source_type=source_type,
            source_id=source_id,
            source_parent_id=source_parent_id,
            source_label=cls._clean(source_label)[:255] or "复习例句",
            source_locator=source_locator,
            english=english,
            chinese=chinese,
            explanation=cls._clean(explanation)[:1000],
        )

    @staticmethod
    def _clean(value):
        return re.sub(r"\s+", " ", str(value or "")).strip()

    @staticmethod
    def _deduplicate(candidates):
        result = []
        seen = set()
        for candidate in candidates:
            key = (
                candidate.source_type,
                candidate.source_id,
                normalize_review_answer(candidate.english),
                normalize_review_answer(candidate.chinese),
            )
            if key not in seen:
                seen.add(key)
                result.append(candidate)
        return result

    @staticmethod
    def _accepted_answers(question):
        try:
            decoded = json.loads(question["accepted_answers_json"])
        except (TypeError, ValueError):
            decoded = []
        answers = [value.strip() for value in decoded if isinstance(value, str) and value.strip()]
        return answers or [question["reference_answer"]]

    def _summary(self, session, questions=None):
        if questions is None:
            questions = self.questions.list_for_session(session["id"])
        return {
            "total": len(questions),
            "answered": sum(question["answered_at"] is not None for question in questions),
            "correct": sum(question["is_correct"] == 1 for question in questions),
        }

    def _question_view(self, question):
        result = {
            "id": question["id"],
            "order": question["question_order"],
            "source": {
                "type": question["source_type"],
                "item_id": question["source_id"],
                "parent_id": question["source_parent_id"],
            },
            "source_label": question["source_label"],
            "question_type": question["question_type"],
            "answer_mode": question["answer_mode"],
            "instruction": "根据中文写出你学过的英文表达。",
            "prompt": question["prompt"],
            "context": question["context_text"] or "",
            "answered": question["answered_at"] is not None,
        }
        if question["answered_at"] is not None:
            result["result"] = {
                "is_correct": question["is_correct"] == 1,
                "submitted_answer": question["submitted_answer"] or "",
                "correct_answer": question["reference_answer"],
                "explanation": question["explanation"] or "",
            }
        return result

    def _answer_view(self, session, question, *, already_answered):
        result = self._question_view(question).get("result")
        return {
            "question_id": question["id"],
            "already_answered": already_answered,
            "is_correct": question["is_correct"] == 1,
            "submitted_answer": question["submitted_answer"] or "",
            "correct_answer": question["reference_answer"],
            "explanation": question["explanation"] or "",
            "summary": self._summary(session),
            "session_completed": session["completed_at"] is not None,
            "result": result,
        }


class LearningReviewQuestionService:
    """Table registration companion; question access is owned by its session."""

    dao_type = LearningReviewQuestionDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


REVIEW_TABLE_SERVICE_TYPES = {
    m.learning_review_session.name: LearningReviewSessionService,
    m.learning_review_question.name: LearningReviewQuestionService,
}
