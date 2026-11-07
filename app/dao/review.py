"""Persistence queries for server-owned active-recall review sessions."""

from sqlalchemy import func

from app import models as m
from app.dao.base import BaseTableDAO


class LearningReviewSessionDAO(BaseTableDAO):
    table = m.learning_review_session

    def get_for_user(self, session_id, user_id):
        return self.find_by_id(session_id, self.table.c.user_id == user_id)

    def mark_completed(self, session_id):
        self.update(session_id, {"completed_at": func.now()})


class LearningReviewQuestionDAO(BaseTableDAO):
    table = m.learning_review_question

    def get_for_session(self, question_id, session_id):
        return self.find_by_id(question_id, self.table.c.session_id == session_id)

    def list_for_session(self, session_id):
        return self.list_where(
            self.table.c.session_id == session_id,
            order_by=[self.table.c.question_order, self.table.c.id],
        )

    def count_answered(self, session_id):
        return self.count(
            self.table.c.session_id == session_id,
            self.table.c.answered_at.is_not(None),
        )

    def count_correct(self, session_id):
        return self.count(
            self.table.c.session_id == session_id,
            self.table.c.is_correct == 1,
        )


REVIEW_TABLE_DAO_TYPES = {
    m.learning_review_session.name: LearningReviewSessionDAO,
    m.learning_review_question.name: LearningReviewQuestionDAO,
}
