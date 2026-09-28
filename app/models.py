"""Mappings for the existing MySQL schema. Schema changes remain explicit SQL migrations."""

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    text,
)

metadata = MetaData()

english_note = Table(
    "english_note",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("note_date", Date, nullable=False),
    Column("title", String(200), nullable=True),
    Column("source", String(100), nullable=True),
    Column("summary", Text, nullable=True),
    Column("share_status", Integer, nullable=False, server_default=text("'0'")),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

english_note_item = Table(
    "english_note_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("note_id", Integer, nullable=False),
    Column("item_order", Integer, nullable=False, server_default=text("'0'")),
    Column("item_type", String(50), nullable=False, server_default=text("'note_block'")),
    Column("item_title", String(255), nullable=True),
    Column("raw_text", Text, nullable=False),
    Column("english_text", Text, nullable=True),
    Column("chinese_text", Text, nullable=True),
    Column("explanation", Text, nullable=True),
    Column("examples", Text, nullable=True),
    Column("example_image_url", String(500), nullable=True),
    Column("example_image_alt", String(255), nullable=True),
    Column("keywords", String(500), nullable=True),
    Column("language_register", String(32), nullable=False, server_default=text("'unclassified'")),
    Column("usage_scenarios_json", Text, nullable=True),
    Column("register_reason", String(500), nullable=True),
    Column("classification_confidence", Integer, nullable=True),
    Column("classification_source", String(32), nullable=False, server_default=text("'unclassified'")),
    Column("share_status", Integer, nullable=False, server_default=text("'0'")),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

everyday_sentence = Table(
    "everyday_sentence",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tag", String(100), nullable=False),
    Column("en", Text, nullable=False),
    Column("cn", Text, nullable=False),
    Column("note", Text, nullable=True),
    Column("share_status", Integer, nullable=False, server_default=text("'0'")),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

interview_answer_section = Table(
    "interview_answer_section",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question_id", Integer, nullable=False),
    Column("section_type", String(50), nullable=False),
    Column("section_title", String(100), nullable=True),
    Column("content_en", Text, nullable=True),
    Column("content_cn", Text, nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

interview_category = Table(
    "interview_category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category_name", String(100), nullable=False),
    Column("category_code", String(50), nullable=False),
    Column("description", String(255), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("status", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("category_code"),
)

interview_question = Table(
    "interview_question",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category_id", Integer, nullable=False),
    Column("question", Text, nullable=False),
    Column("question_cn", Text, nullable=True),
    Column("short_answer", Text, nullable=True),
    Column("full_answer", Text, nullable=True),
    Column("answer_tip", Text, nullable=True),
    Column("keywords", String(500), nullable=True),
    Column("difficulty_level", Integer, nullable=False, server_default=text("'1'")),
    Column("share_status", Integer, nullable=False, server_default=text("'0'")),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("status", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

interview_question_tag = Table(
    "interview_question_tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("question_id", Integer, nullable=False),
    Column("tag_name", String(100), nullable=False),
)

kids_english_card = Table(
    "kids_english_card",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("word", String(100), nullable=False),
    Column("translation", String(255), nullable=False),
    Column("phonics", String(100), nullable=True),
    Column("part_of_speech", String(50), nullable=True),
    Column("level", String(30), nullable=False, server_default=text("'Core'")),
    Column("syllables", String(255), nullable=True),
    Column("stress", String(255), nullable=True),
    Column("phonics_focus", String(255), nullable=True),
    Column("syllable_tip", Text, nullable=True),
    Column("category", String(100), nullable=False),
    Column("emoji", String(32), nullable=True),
    Column("image_url", String(255), nullable=True),
    Column("tip", Text, nullable=True),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_active", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

kids_english_card_example = Table(
    "kids_english_card_example",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, nullable=False),
    Column("example_text", Text, nullable=False),
    Column("translation", Text, nullable=False),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_active", Integer, nullable=False, server_default=text("'1'")),
)

kids_english_card_sound_part = Table(
    "kids_english_card_sound_part",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, nullable=False),
    Column("part_order", Integer, nullable=False),
    Column("chunk", String(100), nullable=False),
    Column("pronunciation", String(100), nullable=False),
    UniqueConstraint("card_id", "part_order"),
)

kids_english_card_word_family = Table(
    "kids_english_card_word_family",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", Integer, nullable=False),
    Column("related_word", String(100), nullable=False),
    Column("part_of_speech", String(50), nullable=True),
    Column("meaning", String(255), nullable=True),
    Column("priority_order", Integer, nullable=False, server_default=text("'0'")),
)

study_progress = Table(
    "study_progress",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("content_type", String(50), nullable=False),
    Column("parent_id", Integer, nullable=True),
    Column("item_id", Integer, nullable=False),
    Column("completed", Integer, nullable=False, server_default=text("'0'")),
    Column("last_studied_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("user_id", "content_type", "parent_id"),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(100), nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("full_name", String(100), nullable=False),
    Column("email", String(150), nullable=True),
    Column("contact_number", String(30), nullable=True),
    Column("home_address", String(255), nullable=True),
    Column("role", String(50), nullable=False, server_default=text("'user'")),
    Column("status", String(50), nullable=False, server_default=text("'active'")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("username"),
    UniqueConstraint("email"),
    UniqueConstraint("contact_number", name="uk_user_contact_number"),
)

login_audit = Table(
    "login_audit",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("username", String(100), nullable=False),
    Column("full_name", String(100), nullable=True),
    Column("login_ip", String(45), nullable=True),
    Column("user_agent", String(1000), nullable=True),
    Column("success", Boolean, nullable=False, server_default=text("1")),
    Column("logged_in_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)
Index("idx_login_audit_logged_in_at", login_audit.c.logged_in_at)
Index("idx_login_audit_user_logged_in_at", login_audit.c.user_id, login_audit.c.logged_in_at)
Index("idx_login_audit_ip_logged_in_at", login_audit.c.login_ip, login_audit.c.logged_in_at)

vocabulary_library = Table(
    "vocabulary_library",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String(100), nullable=False),
    Column("term", String(255), nullable=False),
    Column("chinese_meaning", Text, nullable=True),
    Column("english_note", Text, nullable=True),
    Column("example_sentence", Text, nullable=True),
    Column("extra_note", Text, nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)

math_card = Table(
    "math_card",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", String(100), nullable=False),
    Column("title", String(200), nullable=False),
    Column("summary", Text, nullable=False),
    Column("key_points", Text, nullable=False),
    Column("common_mistakes", Text, nullable=False),
    Column("example_question", Text, nullable=False),
    Column("example_answer", Text, nullable=False),
    Column("example_image_url", String(255), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("0")),
    Column("is_published", Integer, nullable=False, server_default=text("1")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("title"),
)

english_textbook_lesson = Table(
    "english_textbook_lesson",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("unit_name", String(100), nullable=False),
    Column("lesson_name", String(100), nullable=False),
    Column("title", String(255), nullable=False),
    Column("title_cn", String(255), nullable=True),
    Column("summary", Text, nullable=True),
    Column("unit_order", Integer, nullable=False, server_default=text("0")),
    Column("lesson_order", Integer, nullable=False, server_default=text("0")),
    Column("is_published", Integer, nullable=False, server_default=text("1")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("unit_name", "lesson_name"),
)

english_textbook_sentence = Table(
    "english_textbook_sentence",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("lesson_id", Integer, nullable=False),
    Column("sentence_order", Integer, nullable=False, server_default=text("0")),
    Column("english_text", Text, nullable=False),
    Column("chinese_text", Text, nullable=False),
    Column("is_published", Integer, nullable=False, server_default=text("1")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("lesson_id", "sentence_order"),
)

phonics_lesson = Table(
    "phonics_lesson",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("lesson_code", String(80), nullable=False),
    Column("title", String(200), nullable=False),
    Column("subtitle", String(200), nullable=False),
    Column("pattern_text", String(255), nullable=False),
    Column("sound_text", Text, nullable=False),
    Column("learning_tip", Text, nullable=False),
    Column("review_examples_json", Text, nullable=True),
    Column("examples_json", Text, nullable=False),
    Column("quiz_prompt", Text, nullable=False),
    Column("quiz_choices_json", Text, nullable=False),
    Column("quiz_answer", String(255), nullable=False),
    Column("priority_order", Integer, nullable=False, server_default=text("0")),
    Column("is_active", Integer, nullable=False, server_default=text("1")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("lesson_code"),
)

daily_spoken_dialogue_item = Table(
    "daily_spoken_dialogue_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("lesson_code", String(100), nullable=False),
    Column("chapter_title", String(200), nullable=False),
    Column("lesson_title", String(200), nullable=False),
    Column("lesson_order", Integer, nullable=False, server_default=text("0")),
    Column("section_code", String(50), nullable=False),
    Column("section_title", String(200), nullable=False),
    Column("section_order", Integer, nullable=False, server_default=text("0")),
    Column("item_type", String(50), nullable=False),
    Column("item_order", Integer, nullable=False),
    Column("speaker", String(100), nullable=True),
    Column("item_title", String(255), nullable=True),
    Column("english_text", Text, nullable=False),
    Column("chinese_text", Text, nullable=True),
    Column("pronunciation", String(255), nullable=True),
    Column("explanation", Text, nullable=True),
    Column("examples", Text, nullable=True),
    Column("keywords", String(500), nullable=True),
    Column("is_published", Integer, nullable=False, server_default=text("1")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("lesson_code", "item_order"),
)

# The learning catalogue separates learner-facing courses from materials.  A
# course represents the product a learner joins; a material is one whole book,
# card set, question bank, or note collection; material lessons point at the
# existing content roots (or retain a self-contained JSON fallback).
learning_module = Table(
    "learning_module",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("module_code", String(80), nullable=False),
    Column("name", String(100), nullable=False),
    Column("name_en", String(100), nullable=True),
    Column("description", String(500), nullable=True),
    Column("icon", String(32), nullable=True),
    Column("color", String(32), nullable=True),
    Column("route_key", String(100), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_published", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("module_code"),
)
Index("idx_learning_module_published_order", learning_module.c.is_published, learning_module.c.sort_order)

learning_topic = Table(
    "learning_topic",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "module_id",
        Integer,
        ForeignKey("learning_module.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("topic_code", String(100), nullable=False),
    Column("title", String(200), nullable=False),
    Column("title_en", String(200), nullable=True),
    Column("description", Text, nullable=True),
    Column("cover_url", String(500), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_published", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("module_id", "topic_code"),
)
Index(
    "idx_learning_topic_module_published_order",
    learning_topic.c.module_id,
    learning_topic.c.is_published,
    learning_topic.c.sort_order,
)

learning_template = Table(
    "learning_template",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("template_code", String(80), nullable=False),
    Column("template_version", Integer, nullable=False, server_default=text("'1'")),
    Column("name", String(120), nullable=False),
    Column("description", Text, nullable=True),
    Column("content_kind", String(50), nullable=False),
    Column("supported_clients_json", Text, nullable=False, server_default=text("'[]'")),
    Column("config_json", Text, nullable=True),
    Column("status", String(20), nullable=False, server_default=text("'active'")),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("template_code", "template_version"),
)
Index(
    "idx_learning_template_status_order",
    learning_template.c.status,
    learning_template.c.sort_order,
)

learning_material = Table(
    "learning_material",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "topic_id",
        Integer,
        ForeignKey("learning_topic.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "template_id",
        Integer,
        ForeignKey("learning_template.id", ondelete="RESTRICT"),
        nullable=True,
    ),
    Column("material_code", String(120), nullable=False),
    Column("title", String(255), nullable=False),
    Column("title_en", String(255), nullable=True),
    Column("summary", Text, nullable=True),
    Column("material_type", String(50), nullable=False),
    Column("publisher", String(200), nullable=True),
    Column("version_name", String(100), nullable=True),
    Column("cover_url", String(500), nullable=True),
    Column("difficulty_code", String(50), nullable=True),
    Column("estimated_minutes", Integer, nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_published", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("topic_id", "material_code"),
)
Index(
    "idx_learning_material_topic_published_order",
    learning_material.c.topic_id,
    learning_material.c.is_published,
    learning_material.c.sort_order,
)

learning_material_lesson = Table(
    "learning_material_lesson",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "material_id",
        Integer,
        ForeignKey("learning_material.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("lesson_code", String(120), nullable=False),
    Column("title", String(255), nullable=False),
    Column("title_en", String(255), nullable=True),
    Column("summary", Text, nullable=True),
    Column("source_resource", String(80), nullable=True),
    Column("source_reference_id", Integer, nullable=True),
    Column("content_json", Text, nullable=True),
    Column("lesson_format", String(50), nullable=False, server_default=text("'source'")),
    Column("estimated_minutes", Integer, nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_published", Integer, nullable=False, server_default=text("'1'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("material_id", "lesson_code"),
)
Index(
    "idx_learning_material_lesson_material_published_order",
    learning_material_lesson.c.material_id,
    learning_material_lesson.c.is_published,
    learning_material_lesson.c.sort_order,
)
Index(
    "idx_learning_material_lesson_source",
    learning_material_lesson.c.source_resource,
    learning_material_lesson.c.source_reference_id,
)
Index(
    "idx_learning_material_lesson_format",
    learning_material_lesson.c.lesson_format,
    learning_material_lesson.c.is_published,
)

courseware_block = Table(
    "courseware_block",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "material_lesson_id",
        Integer,
        ForeignKey("learning_material_lesson.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("block_code", String(120), nullable=False),
    Column("block_type", String(50), nullable=False),
    Column("title", String(255), nullable=True),
    Column("payload_json", Text, nullable=False),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("status", String(20), nullable=False, server_default=text("'draft'")),
    Column("created_by", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("material_lesson_id", "block_code"),
)
Index(
    "idx_courseware_block_lesson_status_order",
    courseware_block.c.material_lesson_id,
    courseware_block.c.status,
    courseware_block.c.sort_order,
)

courseware_block_source = Table(
    "courseware_block_source",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "courseware_block_id",
        Integer,
        ForeignKey("courseware_block.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("source_resource", String(80), nullable=False),
    Column("source_reference_id", Integer, nullable=False),
    Column("source_field", String(80), nullable=False),
    Column("source_locator_json", Text, nullable=True),
    Column("source_snapshot_text", Text, nullable=False),
    Column("source_hash", String(64), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)
Index(
    "idx_courseware_block_source_block_order",
    courseware_block_source.c.courseware_block_id,
    courseware_block_source.c.sort_order,
)
Index(
    "idx_courseware_block_source_reference",
    courseware_block_source.c.source_resource,
    courseware_block_source.c.source_reference_id,
    courseware_block_source.c.source_field,
)

learning_course = Table(
    "learning_course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "material_id",
        Integer,
        ForeignKey("learning_material.id", ondelete="RESTRICT"),
        nullable=True,
        # Kept as the first linked material for old API clients and existing
        # deployments.  learning_course_material is the authoritative mapping.
    ),
    Column("course_code", String(120), nullable=False),
    Column("title", String(255), nullable=False),
    Column("title_en", String(255), nullable=True),
    Column("summary", Text, nullable=True),
    Column("course_type", String(50), nullable=False, server_default=text("'lesson'")),
    Column("content_resource", String(80), nullable=True),
    Column("content_reference_id", Integer, nullable=True),
    Column("content_json", Text, nullable=True),
    Column("cover_url", String(500), nullable=True),
    Column("estimated_minutes", Integer, nullable=True),
    Column("difficulty_code", String(50), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("is_published", Integer, nullable=False, server_default=text("'1'")),
    Column("access_policy", String(20), nullable=False, server_default=text("'free'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("course_code"),
)
Index("idx_learning_course_material", learning_course.c.material_id)
Index(
    "idx_learning_course_access_published",
    learning_course.c.access_policy,
    learning_course.c.is_published,
)

learning_topic_course = Table(
    "learning_topic_course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "topic_id",
        Integer,
        ForeignKey("learning_topic.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("topic_id", "course_id"),
)
Index(
    "idx_learning_topic_course_topic_order",
    learning_topic_course.c.topic_id,
    learning_topic_course.c.sort_order,
)
Index(
    "idx_learning_topic_course_course",
    learning_topic_course.c.course_id,
)

# A course may arrange several whole materials.  The mapping owns that order;
# lessons remain owned by their material and are never linked directly to a
# course.
learning_course_material = Table(
    "learning_course_material",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "material_id",
        Integer,
        ForeignKey("learning_material.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("course_id", "material_id"),
)
Index(
    "idx_learning_course_material_course_order",
    learning_course_material.c.course_id,
    learning_course_material.c.sort_order,
)
Index(
    "idx_learning_course_material_material",
    learning_course_material.c.material_id,
    learning_course_material.c.sort_order,
)

membership_plan = Table(
    "membership_plan",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("plan_code", String(64), nullable=False),
    Column("name", String(100), nullable=False),
    Column("name_en", String(100), nullable=True),
    Column("description", String(500), nullable=True),
    Column("tier_rank", Integer, nullable=False, server_default=text("'0'")),
    Column("billing_cycle", String(20), nullable=False, server_default=text("'manual'")),
    Column("duration_days", Integer, nullable=True),
    Column("price", Numeric(10, 2), nullable=False, server_default=text("'0.00'")),
    Column("currency", String(3), nullable=False, server_default=text("'CNY'")),
    Column("icon", String(32), nullable=True),
    Column("badge_text", String(50), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("status", String(20), nullable=False, server_default=text("'draft'")),
    Column("is_default", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("plan_code"),
)
Index("idx_membership_plan_status_sort", membership_plan.c.status, membership_plan.c.sort_order)
Index("idx_membership_plan_rank", membership_plan.c.tier_rank)

membership_benefit = Table(
    "membership_benefit",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("benefit_code", String(80), nullable=False),
    Column("name", String(100), nullable=False),
    Column("name_en", String(100), nullable=True),
    Column("description", String(500), nullable=True),
    Column("benefit_type", String(30), nullable=False),
    Column("value_type", String(20), nullable=False),
    Column("unit", String(50), nullable=True),
    Column("scope_json", Text, nullable=True),
    Column("default_value_json", Text, nullable=True),
    Column("icon", String(32), nullable=True),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("status", String(20), nullable=False, server_default=text("'active'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("benefit_code"),
)
Index(
    "idx_membership_benefit_status_sort",
    membership_benefit.c.status,
    membership_benefit.c.sort_order,
)
Index("idx_membership_benefit_type", membership_benefit.c.benefit_type)

membership_plan_benefit = Table(
    "membership_plan_benefit",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "membership_plan_id",
        Integer,
        ForeignKey("membership_plan.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "benefit_id",
        Integer,
        ForeignKey("membership_benefit.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("grant_value_json", Text, nullable=True),
    Column("is_enabled", Integer, nullable=False, server_default=text("'1'")),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("membership_plan_id", "benefit_id"),
)
Index(
    "idx_membership_plan_benefit_enabled_sort",
    membership_plan_benefit.c.membership_plan_id,
    membership_plan_benefit.c.is_enabled,
    membership_plan_benefit.c.sort_order,
)
Index("idx_membership_plan_benefit_benefit", membership_plan_benefit.c.benefit_id)

user_membership = Table(
    "user_membership",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "membership_plan_id",
        Integer,
        ForeignKey("membership_plan.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("status", String(20), nullable=False, server_default=text("'pending'")),
    Column("source", String(30), nullable=False, server_default=text("'manual'")),
    Column("starts_at", DateTime, nullable=False),
    Column("ends_at", DateTime, nullable=True),
    Column("auto_renew", Integer, nullable=False, server_default=text("'0'")),
    Column("external_reference", String(100), nullable=True),
    Column("granted_by", Integer, nullable=True),
    Column("cancelled_at", DateTime, nullable=True),
    Column("cancel_reason", String(500), nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("external_reference"),
)
Index(
    "idx_user_membership_user_status_time",
    user_membership.c.user_id,
    user_membership.c.status,
    user_membership.c.starts_at,
    user_membership.c.ends_at,
)
Index("idx_user_membership_expiry", user_membership.c.status, user_membership.c.ends_at)
Index("idx_user_membership_plan", user_membership.c.membership_plan_id)

membership_benefit_course = Table(
    "membership_benefit_course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "benefit_id",
        Integer,
        ForeignKey("membership_benefit.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("access_action", String(20), nullable=False, server_default=text("'study'")),
    Column("is_enabled", Integer, nullable=False, server_default=text("'1'")),
    Column("sort_order", Integer, nullable=False, server_default=text("'0'")),
    Column("created_by", Integer, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_by", Integer, nullable=True),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("benefit_id", "course_id", "access_action"),
)
Index(
    "idx_membership_benefit_course_course_enabled",
    membership_benefit_course.c.course_id,
    membership_benefit_course.c.is_enabled,
)

learning_user_course = Table(
    "learning_user_course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column(
        "source_membership_id",
        Integer,
        ForeignKey("user_membership.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("source", String(30), nullable=False, server_default=text("'self_added'")),
    Column("status", String(20), nullable=False, server_default=text("'active'")),
    Column("enrolled_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_opened_at", DateTime, nullable=True),
    Column("archived_at", DateTime, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("user_id", "course_id"),
)
Index(
    "idx_learning_user_course_user_status_opened",
    learning_user_course.c.user_id,
    learning_user_course.c.status,
    learning_user_course.c.last_opened_at,
)
Index("idx_learning_user_course_course", learning_user_course.c.course_id)

# study_progress remains the compatibility store for legacy note and sentence
# pages. New module → topic → course learning uses the three tables below.
learning_progress = Table(
    "learning_progress",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("status", String(20), nullable=False, server_default=text("'in_progress'")),
    Column("total_item_count", Integer, nullable=False, server_default=text("'0'")),
    Column("completed_item_count", Integer, nullable=False, server_default=text("'0'")),
    Column("last_item_key", String(160), nullable=True),
    Column("last_item_id", Integer, nullable=True),
    Column("last_position_seconds", Integer, nullable=False, server_default=text("'0'")),
    Column("started_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_studied_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("completed_at", DateTime, nullable=True),
    Column("accumulated_seconds", Integer, nullable=False, server_default=text("'0'")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("user_id", "course_id"),
)
Index(
    "idx_learning_progress_user_status_last_studied",
    learning_progress.c.user_id,
    learning_progress.c.status,
    learning_progress.c.last_studied_at,
)
Index("idx_learning_progress_course", learning_progress.c.course_id)

learning_progress_item = Table(
    "learning_progress_item",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "progress_id",
        Integer,
        ForeignKey("learning_progress.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("item_key", String(160), nullable=False),
    Column("item_type", String(50), nullable=False, server_default=text("'course_item'")),
    Column("item_reference_id", Integer, nullable=True),
    Column("is_completed", Integer, nullable=False, server_default=text("'0'")),
    Column("last_position_seconds", Integer, nullable=False, server_default=text("'0'")),
    Column("attempt_count", Integer, nullable=False, server_default=text("'0'")),
    Column("score", Integer, nullable=True),
    Column("started_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_studied_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("completed_at", DateTime, nullable=True),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("progress_id", "item_key"),
)
Index(
    "idx_learning_progress_item_progress_completed",
    learning_progress_item.c.progress_id,
    learning_progress_item.c.is_completed,
)

learning_study_session = Table(
    "learning_study_session",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column(
        "progress_id",
        Integer,
        ForeignKey("learning_progress.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "course_id",
        Integer,
        ForeignKey("learning_course.id", ondelete="RESTRICT"),
        nullable=False,
    ),
    Column("platform", String(30), nullable=False, server_default=text("'web'")),
    Column("entry_source", String(100), nullable=True),
    Column("started_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("last_heartbeat_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("ended_at", DateTime, nullable=True),
    Column("active_seconds", Integer, nullable=False, server_default=text("'0'")),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)
Index(
    "idx_learning_study_session_user_started",
    learning_study_session.c.user_id,
    learning_study_session.c.started_at,
)
Index(
    "idx_learning_study_session_course_started",
    learning_study_session.c.course_id,
    learning_study_session.c.started_at,
)
Index(
    "idx_learning_study_session_progress_open",
    learning_study_session.c.progress_id,
    learning_study_session.c.ended_at,
)
