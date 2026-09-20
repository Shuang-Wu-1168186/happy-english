from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app import models as m
from app.core.security import hash_password


def sample_engine(url="sqlite://"):
    options = {"poolclass": StaticPool} if url == "sqlite://" else {}
    engine = create_engine(url, connect_args={"check_same_thread": False}, **options)
    m.metadata.create_all(engine)
    with engine.begin() as c:
        c.execute(
            m.user.insert(),
            [
                {
                    "id": 1,
                    "username": "admin_test",
                    "full_name": "测试管理员",
                    "role": "admin",
                    "password_hash": hash_password("Testing123!"),
                },
                {
                    "id": 2,
                    "username": "learner_test",
                    "full_name": "学习者",
                    "role": "learner",
                    "password_hash": hash_password("Testing123!"),
                },
            ],
        )
        c.execute(
            m.everyday_sentence.insert(),
            [
                {
                    "id": 1,
                    "tag": "Greetings",
                    "en": "Hello, how are you?",
                    "cn": "你好，最近怎么样？",
                    "created_by": 1,
                },
                {
                    "id": 2,
                    "tag": "Greetings",
                    "en": "Nice to meet you.",
                    "cn": "很高兴见到你。",
                    "created_by": 1,
                },
            ],
        )
        c.execute(
            m.english_note.insert(),
            {"id": 1, "note_date": date(2026, 9, 20), "title": "Daily practice", "created_by": 1},
        )
        c.execute(
            m.english_note_item.insert(),
            {
                "id": 1,
                "note_id": 1,
                "item_title": "A useful phrase",
                "raw_text": "Good morning",
                "english_text": "Good morning",
                "chinese_text": "早上好",
                "created_by": 1,
            },
        )
        c.execute(
            m.vocabulary_library.insert(),
            {"id": 1, "category": "Work", "term": "collaborate", "chinese_meaning": "合作"},
        )
        c.execute(
            m.interview_category.insert(),
            {"id": 1, "category_name": "General", "category_code": "general", "created_by": 1},
        )
        c.execute(
            m.interview_question.insert(),
            {"id": 1, "category_id": 1, "question": "Tell me about yourself.", "created_by": 1},
        )
        c.execute(
            m.kids_english_card.insert(),
            {"id": 1, "word": "apple", "translation": "苹果", "category": "Fruit"},
        )
        c.execute(
            m.kids_english_card_example.insert(),
            {"card_id": 1, "example_text": "I like apples.", "translation": "我喜欢苹果。"},
        )
        c.execute(
            m.math_card.insert(),
            {
                "id": 1,
                "category": "Fractions",
                "title": "Fractions",
                "summary": "Parts of a whole",
                "key_points": "Numerator and denominator",
                "common_mistakes": "Keep the denominator",
                "example_question": "1/2 + 1/2",
                "example_answer": "1",
            },
        )
        c.execute(
            m.english_textbook_lesson.insert(),
            {"id": 1, "unit_name": "Unit 1", "lesson_name": "Lesson 1", "title": "Hello"},
        )
        c.execute(
            m.english_textbook_sentence.insert(),
            {"lesson_id": 1, "english_text": "Hello!", "chinese_text": "你好！"},
        )
        c.execute(
            m.phonics_lesson.insert(),
            {
                "id": 1,
                "lesson_code": "short-a",
                "title": "Short A",
                "subtitle": "The short a sound",
                "pattern_text": "a",
                "sound_text": "/æ/",
                "learning_tip": "Open your mouth.",
                "examples_json": '[{"word":"cat","sound":"kæt"}]',
                "quiz_prompt": "Which word has a short a?",
                "quiz_choices_json": '["cat","dog"]',
                "quiz_answer": "cat",
            },
        )
        c.execute(
            m.daily_spoken_dialogue_item.insert(),
            {
                "id": 1,
                "lesson_code": "shopping",
                "chapter_title": "Shopping",
                "lesson_title": "Buy a shirt",
                "section_code": "dialogue",
                "section_title": "At the shop",
                "item_type": "dialogue",
                "item_order": 1,
                "english_text": "How much is this?",
                "chinese_text": "这件多少钱？",
            },
        )
    return engine
