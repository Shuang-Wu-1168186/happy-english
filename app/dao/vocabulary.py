"""Persistence queries for vocabulary decks, cards, and review state."""

from sqlalchemy import and_, case, func, literal, or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class VocabularyDeckDAO(BaseTableDAO):
    table = m.vocabulary_deck

    def find_by_code(self, deck_code):
        return (
            self.db.execute(select(self.table).where(self.table.c.deck_code == deck_code))
            .mappings()
            .first()
        )

    def list_published(self):
        return self.list_where(
            self.table.c.is_published == 1,
            order_by=[self.table.c.sort_order, self.table.c.id],
        )

    def list_library(self, user_id=None):
        """Return published decks with their enabled-card and learner counts."""

        deck_word = m.vocabulary_deck_word
        word = m.vocabulary_word
        progress = m.user_vocabulary_progress
        active_cards = deck_word.join(word, word.c.id == deck_word.c.word_id)
        source = self.table.outerjoin(
            active_cards,
            and_(
                deck_word.c.deck_id == self.table.c.id,
                deck_word.c.is_enabled == 1,
                word.c.is_active == 1,
            ),
        )
        columns = [*self.table.c, func.count(deck_word.c.id).label("word_count")]
        if user_id is not None:
            source = source.outerjoin(
                progress,
                and_(
                    progress.c.deck_word_id == deck_word.c.id,
                    progress.c.user_id == user_id,
                ),
            )
            columns.extend(
                [
                    func.coalesce(
                        func.sum(case((progress.c.id.is_not(None), 1), else_=0)), 0
                    ).label("started_count"),
                    func.coalesce(
                        func.sum(case((progress.c.learning_state == "mastered", 1), else_=0)), 0
                    ).label("mastered_count"),
                ]
            )
        else:
            columns.extend(
                [
                    literal(0).label("started_count"),
                    literal(0).label("mastered_count"),
                ]
            )
        return (
            self.db.execute(
                select(*columns)
                .select_from(source)
                .where(self.table.c.is_published == 1)
                .group_by(*self.table.c)
                .order_by(self.table.c.sort_order, self.table.c.id)
            )
            .mappings()
            .all()
        )

    def list_study_cards(self, deck_id, user_id=None):
        """Load each enabled deck card with its primary sense and example."""

        deck_word = m.vocabulary_deck_word
        word = m.vocabulary_word
        sense = m.vocabulary_word_sense
        example = m.vocabulary_word_example
        progress = m.user_vocabulary_progress
        primary_sense = sense.alias("primary_sense")
        primary_example = example.alias("primary_example")
        first_sense_id = (
            select(primary_sense.c.id)
            .where(primary_sense.c.word_id == word.c.id)
            .order_by(primary_sense.c.sort_order, primary_sense.c.id)
            .limit(1)
            .scalar_subquery()
        )
        first_example_id = (
            select(primary_example.c.id)
            .where(primary_example.c.sense_id == sense.c.id)
            .order_by(primary_example.c.sort_order, primary_example.c.id)
            .limit(1)
            .scalar_subquery()
        )
        columns = [
            deck_word.c.id.label("deck_word_id"),
            deck_word.c.deck_id,
            deck_word.c.sort_order.label("card_sort_order"),
            word.c.id.label("word_id"),
            word.c.word,
            word.c.normalized_word,
            word.c.phonetic_uk,
            word.c.phonetic_us,
            word.c.audio_url,
            word.c.word_level,
            sense.c.id.label("sense_id"),
            sense.c.part_of_speech,
            sense.c.translation,
            sense.c.definition,
            sense.c.memory_hint,
            example.c.id.label("example_id"),
            example.c.english_text.label("example_english_text"),
            example.c.chinese_text.label("example_chinese_text"),
        ]
        source = (
            deck_word.join(word, word.c.id == deck_word.c.word_id)
            .outerjoin(sense, sense.c.id == first_sense_id)
            .outerjoin(example, example.c.id == first_example_id)
        )
        if user_id is not None:
            source = source.outerjoin(
                progress,
                and_(
                    progress.c.deck_word_id == deck_word.c.id,
                    progress.c.user_id == user_id,
                ),
            )
            columns.extend(
                [
                    progress.c.id.label("progress_id"),
                    progress.c.learning_state,
                    progress.c.mastery_level,
                    progress.c.is_marked,
                    progress.c.seen_count,
                    progress.c.review_count,
                    progress.c.correct_count,
                    progress.c.last_rating,
                    progress.c.last_reviewed_at,
                    progress.c.next_review_at,
                ]
            )
        return (
            self.db.execute(
                select(*columns)
                .select_from(source)
                .where(
                    deck_word.c.deck_id == deck_id,
                    deck_word.c.is_enabled == 1,
                    word.c.is_active == 1,
                )
                .order_by(deck_word.c.sort_order, deck_word.c.id)
            )
            .mappings()
            .all()
        )


class VocabularyWordDAO(BaseTableDAO):
    table = m.vocabulary_word

    def find_by_normalized_word(self, normalized_word):
        return (
            self.db.execute(
                select(self.table).where(self.table.c.normalized_word == normalized_word.lower())
            )
            .mappings()
            .first()
        )

    def search(self, query, limit=20):
        query = (query or "").strip()
        if not query:
            return []
        return (
            self.db.execute(
                select(self.table)
                .where(
                    self.table.c.is_active == 1,
                    or_(
                        self.table.c.word.ilike(f"%{query}%"),
                        self.table.c.normalized_word.ilike(f"%{query.lower()}%"),
                    ),
                )
                .order_by(self.table.c.normalized_word, self.table.c.id)
                .limit(limit)
            )
            .mappings()
            .all()
        )

    def list_senses(self, word_id):
        sense = m.vocabulary_word_sense
        return (
            self.db.execute(
                select(sense)
                .where(sense.c.word_id == word_id)
                .order_by(sense.c.sort_order, sense.c.id)
            )
            .mappings()
            .all()
        )

    def detail(self, word_id):
        word = self.find_by_id(word_id)
        if not word:
            return None
        example = m.vocabulary_word_example
        senses = [dict(row) for row in self.list_senses(word_id)]
        if senses:
            examples = self.db.execute(
                select(example)
                .where(example.c.sense_id.in_([sense["id"] for sense in senses]))
                .order_by(example.c.sense_id, example.c.sort_order, example.c.id)
            ).mappings()
            examples_by_sense = {}
            for row in examples:
                examples_by_sense.setdefault(row["sense_id"], []).append(dict(row))
            for sense in senses:
                sense["examples"] = examples_by_sense.get(sense["id"], [])
        return {"word": dict(word), "senses": senses}


class VocabularyWordSenseDAO(BaseTableDAO):
    table = m.vocabulary_word_sense

    def list_for_word(self, word_id):
        return self.list_where(
            self.table.c.word_id == word_id,
            order_by=[self.table.c.sort_order, self.table.c.id],
        )


class VocabularyWordExampleDAO(BaseTableDAO):
    table = m.vocabulary_word_example

    def list_for_sense(self, sense_id):
        return self.list_where(
            self.table.c.sense_id == sense_id,
            order_by=[self.table.c.sort_order, self.table.c.id],
        )


class VocabularyDeckWordDAO(BaseTableDAO):
    table = m.vocabulary_deck_word

    def find_published_for_word(self, word_id):
        deck = m.vocabulary_deck
        return (
            self.db.execute(
                select(self.table)
                .join(deck, deck.c.id == self.table.c.deck_id)
                .where(
                    self.table.c.word_id == word_id,
                    self.table.c.is_enabled == 1,
                    deck.c.is_published == 1,
                )
                .order_by(deck.c.sort_order, deck.c.id, self.table.c.sort_order, self.table.c.id)
                .limit(1)
            )
            .mappings()
            .first()
        )

    def find_for_deck_word(self, deck_id, word_id):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.deck_id == deck_id,
                    self.table.c.word_id == word_id,
                )
            )
            .mappings()
            .first()
        )

    def list_for_deck(self, deck_id, enabled_only=True):
        conditions = [self.table.c.deck_id == deck_id]
        if enabled_only:
            conditions.append(self.table.c.is_enabled == 1)
        return self.list_where(
            *conditions,
            order_by=[self.table.c.sort_order, self.table.c.id],
        )


class UserVocabularyProgressDAO(BaseTableDAO):
    table = m.user_vocabulary_progress

    def find_for_user_card(self, user_id, deck_word_id):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.user_id == user_id,
                    self.table.c.deck_word_id == deck_word_id,
                )
            )
            .mappings()
            .first()
        )

    def list_for_user_deck(self, user_id, deck_id):
        deck_word = m.vocabulary_deck_word
        return (
            self.db.execute(
                select(self.table)
                .join(deck_word, deck_word.c.id == self.table.c.deck_word_id)
                .where(self.table.c.user_id == user_id, deck_word.c.deck_id == deck_id)
                .order_by(deck_word.c.sort_order, deck_word.c.id)
            )
            .mappings()
            .all()
        )

    def list_due_for_user(self, user_id, deck_id=None, now=None, limit=50):
        deck_word = m.vocabulary_deck_word
        word = m.vocabulary_word
        review_time = now if now is not None else func.now()
        conditions = [
            self.table.c.user_id == user_id,
            deck_word.c.is_enabled == 1,
            word.c.is_active == 1,
            or_(
                self.table.c.is_marked == 1,
                and_(
                    self.table.c.next_review_at.is_not(None),
                    self.table.c.next_review_at <= review_time,
                ),
            ),
        ]
        if deck_id is not None:
            conditions.append(deck_word.c.deck_id == deck_id)
        return (
            self.db.execute(
                select(
                    self.table,
                    deck_word.c.deck_id,
                    deck_word.c.word_id,
                    deck_word.c.sort_order.label("card_sort_order"),
                    word.c.word,
                    word.c.phonetic_uk,
                    word.c.phonetic_us,
                )
                .join(deck_word, deck_word.c.id == self.table.c.deck_word_id)
                .join(word, word.c.id == deck_word.c.word_id)
                .where(*conditions)
                .order_by(
                    case((self.table.c.is_marked == 1, 0), else_=1),
                    case((self.table.c.next_review_at.is_(None), 1), else_=0),
                    self.table.c.next_review_at,
                    deck_word.c.sort_order,
                    deck_word.c.id,
                )
                .limit(limit)
            )
            .mappings()
            .all()
        )

    def deck_summary(self, user_id, deck_id):
        deck_word = m.vocabulary_deck_word
        word = m.vocabulary_word
        source = (
            deck_word.join(word, word.c.id == deck_word.c.word_id)
            .outerjoin(
                self.table,
                and_(
                    self.table.c.deck_word_id == deck_word.c.id,
                    self.table.c.user_id == user_id,
                ),
            )
        )
        return (
            self.db.execute(
                select(
                    func.count(deck_word.c.id).label("total_count"),
                    func.coalesce(
                        func.sum(case((self.table.c.id.is_not(None), 1), else_=0)), 0
                    ).label("started_count"),
                    func.coalesce(
                        func.sum(case((self.table.c.learning_state == "mastered", 1), else_=0)), 0
                    ).label("mastered_count"),
                    func.coalesce(
                        func.sum(case((self.table.c.is_marked == 1, 1), else_=0)), 0
                    ).label("marked_count"),
                )
                .select_from(source)
                .where(
                    deck_word.c.deck_id == deck_id,
                    deck_word.c.is_enabled == 1,
                    word.c.is_active == 1,
                )
            )
            .mappings()
            .one()
        )

    def upsert(self, values):
        """Persist one learner/card state across SQLite tests and MySQL."""

        values = dict(values)
        user_id = values["user_id"]
        deck_word_id = values["deck_word_id"]
        values["updated_at"] = func.now()
        update_fields = (
            "learning_state",
            "mastery_level",
            "is_marked",
            "seen_count",
            "review_count",
            "correct_count",
            "last_rating",
            "last_reviewed_at",
            "next_review_at",
        )
        update_values = {name: values[name] for name in update_fields if name in values}
        update_values["updated_at"] = func.now()
        dialect = self.db.get_bind().dialect.name
        if dialect in {"mysql", "mariadb"}:
            from sqlalchemy.dialects.mysql import insert

            statement = insert(self.table).values(**values).on_duplicate_key_update(**update_values)
        elif dialect == "sqlite":
            from sqlalchemy.dialects.sqlite import insert

            statement = insert(self.table).values(**values).on_conflict_do_update(
                index_elements=["user_id", "deck_word_id"],
                set_=update_values,
            )
        else:
            existing = self.find_for_user_card(user_id, deck_word_id)
            if existing:
                self.update(existing["id"], update_values)
            else:
                self.insert(values)
            return self.find_for_user_card(user_id, deck_word_id)
        self.db.execute(statement)
        return self.find_for_user_card(user_id, deck_word_id)

    def set_marked(self, user_id, deck_word_id, is_marked):
        progress = self.find_for_user_card(user_id, deck_word_id)
        if progress:
            self.update(progress["id"], {"is_marked": int(bool(is_marked))})
            return self.find_for_user_card(user_id, deck_word_id)
        return self.upsert(
            {
                "user_id": user_id,
                "deck_word_id": deck_word_id,
                "is_marked": int(bool(is_marked)),
            }
        )


class VocabularyReviewLogDAO(BaseTableDAO):
    table = m.vocabulary_review_log

    def record(self, values):
        return self.insert(values)

    def list_for_user_card(self, user_id, deck_word_id, limit=100):
        return (
            self.db.execute(
                select(self.table)
                .where(
                    self.table.c.user_id == user_id,
                    self.table.c.deck_word_id == deck_word_id,
                )
                .order_by(self.table.c.reviewed_at.desc(), self.table.c.id.desc())
                .limit(limit)
            )
            .mappings()
            .all()
        )


VOCABULARY_TABLE_DAO_TYPES = {
    m.vocabulary_deck.name: VocabularyDeckDAO,
    m.vocabulary_word.name: VocabularyWordDAO,
    m.vocabulary_word_sense.name: VocabularyWordSenseDAO,
    m.vocabulary_word_example.name: VocabularyWordExampleDAO,
    m.vocabulary_deck_word.name: VocabularyDeckWordDAO,
    m.user_vocabulary_progress.name: UserVocabularyProgressDAO,
    m.vocabulary_review_log.name: VocabularyReviewLogDAO,
}
