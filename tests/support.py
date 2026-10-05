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
            m.learning_module.insert(),
            [
                {
                    "id": 1,
                    "module_code": "beginner-english",
                    "name": "入门英语",
                    "name_en": "Beginner English",
                    "route_key": "phonics",
                    "sort_order": 10,
                },
                {
                    "id": 2,
                    "module_code": "elementary-english",
                    "name": "初级英语",
                    "name_en": "Elementary English",
                    "route_key": "dialogues",
                    "sort_order": 20,
                },
                {
                    "id": 3,
                    "module_code": "intermediate-english",
                    "name": "中级英语",
                    "name_en": "Intermediate English",
                    "route_key": "intermediate",
                    "sort_order": 30,
                },
                {
                    "id": 4,
                    "module_code": "advanced-english",
                    "name": "进阶英语",
                    "name_en": "Advanced English",
                    "route_key": "advanced",
                    "sort_order": 40,
                },
                {
                    "id": 5,
                    "module_code": "higher-english",
                    "name": "高级英语",
                    "name_en": "Higher English",
                    "route_key": "higher",
                    "sort_order": 50,
                },
                {
                    "id": 6,
                    "module_code": "private-zone",
                    "name": "私人专区",
                    "name_en": "Private Zone",
                    "route_key": "private",
                    "sort_order": 60,
                },
            ],
        )
        c.execute(
            m.learning_topic.insert(),
            [
                {
                    "id": 1,
                    "module_id": 2,
                    "topic_code": "english-textbook",
                    "title": "英文课本",
                    "title_en": "English Textbook",
                    "description": "跟着课文听读、理解和练习，按单元建立扎实基础。",
                    "sort_order": 10,
                    "is_published": 0,
                },
                {
                    "id": 2,
                    "module_id": 1,
                    "topic_code": "natural-phonics",
                    "title": "自然拼读专区",
                    "title_en": "Natural Phonics",
                    "description": "从字母、音素和拼读规律开始，练出见词能读的能力。",
                    "sort_order": 10,
                    "is_published": 1,
                },
                {
                    "id": 3,
                    "module_id": 2,
                    "topic_code": "textbook-vocabulary",
                    "title": "课本单词",
                    "title_en": "Textbook Vocabulary",
                    "description": "围绕课本单元积累核心单词、发音和例句。",
                    "sort_order": 30,
                    "is_published": 0,
                },
                {
                    "id": 4,
                    "module_id": 4,
                    "topic_code": "daily-speaking-practice",
                    "title": "每日口语",
                    "title_en": "Daily Speaking",
                    "description": "每天练习实用句子和短语，让开口成为自然习惯。",
                    "sort_order": 10,
                    "is_published": 0,
                },
                {
                    "id": 5,
                    "module_id": 2,
                    "topic_code": "daily-speaking-dialogues",
                    "title": "日常口语专区",
                    "title_en": "Daily Spoken English",
                    "description": "围绕真实生活场景学习成组对话，练习自然回应。",
                    "sort_order": 10,
                    "is_published": 1,
                },
                {
                    "id": 6,
                    "module_id": 5,
                    "topic_code": "interview-english",
                    "title": "面试英语",
                    "title_en": "Interview English",
                    "description": "围绕自我介绍、常见问题和完整回答，做好求职面试准备。",
                    "sort_order": 10,
                    "is_published": 0,
                },
                {
                    "id": 7,
                    "module_id": 5,
                    "topic_code": "professional-vocabulary",
                    "title": "专业词汇",
                    "title_en": "Professional Vocabulary",
                    "description": "积累工作、技术和专业沟通常用的词汇与表达。",
                    "sort_order": 20,
                    "is_published": 0,
                },
                {
                    "id": 8,
                    "module_id": 6,
                    "topic_code": "my-english-notes",
                    "title": "我的英语笔记",
                    "title_en": "My English Notes",
                    "description": "整理个人学习笔记、卡片和复习内容。",
                    "sort_order": 10,
                    "is_published": 1,
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
    return engine
