from datetime import date, datetime
from decimal import Decimal
import json
import math
import re
from typing import Any, Literal
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

Role = Literal["user", "learner", "premium_learner", "volunteer", "leader", "admin"]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


def valid_private_zone_target_url(value: str):
    target = value.strip()
    if target.startswith("/") and not target.startswith("//"):
        return target
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return target
    raise ValueError("Use a HappyEnglish path beginning with / or an HTTP(S) URL.")


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=72)


class MiniProgramLoginInput(Input):
    login_code: str = Field(min_length=1, max_length=512)
    phone_code: str = Field(min_length=1, max_length=512)


class ProfileInput(Input):
    full_name: str = Field(min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=150)
    contact_number: str | None = Field(default=None, max_length=30)
    home_address: str | None = Field(default=None, max_length=255)

    @field_validator("email", "contact_number", "home_address", mode="before")
    @classmethod
    def blank_optional_text_is_none(cls, value):
        return None if isinstance(value, str) and not value.strip() else value

    @field_validator("email")
    @classmethod
    def valid_email(cls, value):
        if value and ("@" not in value or "." not in value.rsplit("@", 1)[-1]):
            raise ValueError("Enter a valid email address.")
        return value or None


def strong_password(value: str):
    if len(value) < 8 or len(value.encode()) > 72:
        raise ValueError("Password must be at least 8 characters and at most 72 UTF-8 bytes.")
    if (
        sum(
            (
                any(c.islower() for c in value),
                any(c.isupper() for c in value),
                any(c.isdigit() for c in value),
                any(not c.isalnum() for c in value),
            )
        )
        < 3
    ):
        raise ValueError("Use at least three of: uppercase, lowercase, digits and symbols.")
    return value


class SignupInput(ProfileInput):
    username: str = Field(pattern=r"^\w{3,50}$")
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return strong_password(value)


class AdminCreateInput(SignupInput):
    role: Role = "learner"
    status: Literal["active", "inactive"] = "active"


class AdminUpdateInput(ProfileInput):
    username: str = Field(pattern=r"^\w{3,50}$")
    role: Role
    status: Literal["active", "inactive"]


class PasswordInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    old_password: str = Field(min_length=1, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        return strong_password(value)


class NoteInput(Input):
    note_date: date
    title: str = Field(min_length=1, max_length=200)
    source: str = Field(default="", max_length=100)
    summary: str = Field(default="", max_length=20000)
    share_status: Literal[0, 1] = 0
    priority_order: int = 0


class NoteItemInput(Input):
    note_id: int = Field(gt=0)
    item_type: str = Field(default="knowledge", min_length=1, max_length=50)
    item_title: str = Field(min_length=1, max_length=255)
    raw_text: str = Field(min_length=1, max_length=50000)
    english_text: str = Field(min_length=1, max_length=50000)
    chinese_text: str = Field(min_length=1, max_length=50000)
    explanation: str = Field(default="", max_length=50000)
    examples: str = Field(default="", max_length=50000)
    example_image_url: str = Field(default="", max_length=500, validate_default=True)
    example_image_alt: str = Field(default="", max_length=255)
    keywords: str = Field(default="", max_length=500)
    language_register: Literal[
        "common_spoken",
        "formal_spoken",
        "written",
        "mixed",
        "neutral",
        "reference",
        "unclassified",
    ] | None = None
    usage_scenarios: list[
        Literal[
            "daily_life",
            "friends_social",
            "workplace",
            "meeting_presentation",
            "customer_service",
            "interview",
            "travel_service",
            "email_writing",
            "report_writing",
            "academic",
            "technical",
            "health_medical",
            "online_chat",
            "general",
        ]
    ] | None = Field(default=None, max_length=3)
    register_reason: str | None = Field(default=None, max_length=500)
    share_status: Literal[0, 1] = 0
    priority_order: int = 0

    @field_validator("example_image_url")
    @classmethod
    def valid_image_url(cls, value):
        url = value.strip()
        if not url:
            raise ValueError("请上传笔记图片或填写图片地址。")
        if not url.startswith(("https://", "http://", "/static/")):
            raise ValueError("Use an HTTP(S) image URL or an uploaded /static/ image.")
        return url


class NoteItemLanguageRegisterInput(Input):
    """The two quick labels available while browsing note cards on the web."""

    language_register: Literal["common_spoken", "formal_spoken"]


class SentenceInput(Input):
    tag: str = Field(default="Everyday Speaking", max_length=100)
    en: str = Field(min_length=1, max_length=20000)
    cn: str = Field(min_length=1, max_length=20000)
    note: str = Field(default="", max_length=20000)
    share_status: Literal[0, 1] = 0
    priority_order: int = 0


class VocabularyInput(Input):
    category: str = Field(default="professional vocabulary", min_length=1, max_length=100)
    term: str = Field(min_length=1, max_length=255)
    chinese_meaning: str = Field(min_length=1, max_length=20000)
    english_note: str = Field(default="", max_length=20000)
    example_sentence: str = Field(default="", max_length=20000)
    extra_note: str = Field(default="", max_length=20000)
    sort_order: int = 0


class AnswerSection(Input):
    section_type: Literal["situation", "action", "result", "learning"]
    section_title: str = Field(max_length=100)
    content_en: str = Field(default="", max_length=30000)
    content_cn: str = Field(default="", max_length=30000)


class InterviewInput(Input):
    category_id: int = Field(gt=0)
    question: str = Field(min_length=1, max_length=20000)
    question_cn: str = Field(default="", max_length=20000)
    short_answer: str = Field(default="", max_length=30000)
    full_answer: str = Field(default="", max_length=50000)
    answer_tip: str = Field(default="", max_length=20000)
    keywords: str = Field(default="", max_length=500)
    difficulty_level: int = Field(default=1, ge=1, le=3)
    share_status: Literal[0, 1] = 0
    priority_order: int = 0
    sections: list[AnswerSection] = Field(default_factory=list, max_length=4)

    @field_validator("sections")
    @classmethod
    def unique_sections(cls, sections):
        if len({s.section_type for s in sections}) != len(sections):
            raise ValueError("Answer sections must be unique.")
        return sections


class ProgressInput(Input):
    content_type: Literal["english_note", "everyday_sentence"]
    parent_id: int = Field(default=0, ge=0)
    item_id: int = Field(gt=0)
    completed: bool = False


class TTSInput(Input):
    text: str = Field(min_length=1, max_length=1000)
    lang: Literal["b", "z"] = "b"
    speed: float = Field(default=1, ge=0.5, le=2, allow_inf_nan=False)
    cache: bool = True


class NoteTTSInput(Input):
    item_id: int = Field(gt=0)


class FamilyGroupInput(Input):
    name: str = Field(min_length=1, max_length=120)


class FamilyGroupMemberInput(Input):
    user_id: int | None = Field(default=None, gt=0)
    username: str = Field(default="", max_length=100)
    role: Literal["member", "admin"] = "member"


class FamilyGroupJoinInput(Input):
    invite_code: str = Field(min_length=6, max_length=32)


class PrivateZoneFeatureInput(Input):
    title: str = Field(min_length=1, max_length=120)
    title_en: str = Field(default="", max_length=120)
    description: str = Field(default="", max_length=500)
    icon: str = Field(default="", max_length=32)
    route_key: str = Field(min_length=1, max_length=100)
    target_url: str = Field(min_length=1, max_length=1000)
    config: dict[str, Any] = Field(default_factory=dict)
    sort_order: int = 0
    is_enabled: Literal[0, 1] = 1

    @field_validator("target_url")
    @classmethod
    def valid_target_url(cls, value):
        return valid_private_zone_target_url(value)


class PrivateZoneItemInput(Input):
    scope_type: Literal["personal", "family"]
    family_group_id: int | None = Field(default=None, gt=0)
    resource_type: Literal["material", "course", "note", "note_item"]
    resource_id: int = Field(gt=0)
    label: str = Field(default="", max_length=255)
    sort_order: int = 0


class PrivateZoneNoteInput(Input):
    note_date: date
    title: str = Field(min_length=1, max_length=200)
    source: str = Field(default="", max_length=100)
    summary: str = Field(default="", max_length=20000)
    scope_type: Literal["personal", "family"]
    family_group_id: int | None = Field(default=None, gt=0)
    priority_order: int = 0


class PrivateZoneNoteItemInput(Input):
    item_type: str = Field(default="knowledge", min_length=1, max_length=50)
    item_title: str = Field(min_length=1, max_length=255)
    raw_text: str = Field(min_length=1, max_length=50000)
    english_text: str = Field(min_length=1, max_length=50000)
    chinese_text: str = Field(min_length=1, max_length=50000)
    explanation: str = Field(default="", max_length=50000)
    examples: str = Field(default="", max_length=50000)
    example_image_url: str = Field(default="", max_length=500)
    example_image_alt: str = Field(default="", max_length=255)
    keywords: str = Field(default="", max_length=500)
    priority_order: int = 0


class PrivateZoneShortcutInput(Input):
    family_group_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=120)
    target_url: str = Field(min_length=1, max_length=1000)
    description: str = Field(default="", max_length=500)
    icon: str = Field(default="", max_length=32)
    sort_order: int = 0

    @field_validator("target_url")
    @classmethod
    def valid_target_url(cls, value):
        return valid_private_zone_target_url(value)


class PersonalNoteInput(Input):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="", max_length=50000)
    tags: str = Field(default="", max_length=500)
    color: str = Field(default="", max_length=32)
    is_pinned: Literal[0, 1] = 0


class LearningModuleInput(Input):
    module_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,79}$")
    module_type: Literal["level", "training", "resource"] = "level"
    name: str = Field(min_length=1, max_length=100)
    name_en: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=500)
    icon: str = Field(default="", max_length=32)
    color: str = Field(default="", max_length=32)
    route_key: str = Field(default="", max_length=100)
    sort_order: int = 0
    is_published: Literal[0, 1] = 1


class LearningTopicInput(Input):
    module_id: int = Field(gt=0)
    topic_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,99}$")
    title: str = Field(min_length=1, max_length=200)
    title_en: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=50000)
    cover_url: str = Field(default="", max_length=500)
    sort_order: int = 0
    is_published: Literal[0, 1] = 1


class LearningTrainingItemInput(Input):
    """One playable item in a training module, such as a podcast episode."""

    module_id: int = Field(gt=0)
    resource_type: Literal["podcast", "speaking"] = "podcast"
    item_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,99}$")
    title: str = Field(min_length=1, max_length=200)
    title_en: str = Field(default="", max_length=200)
    summary: str = Field(default="", max_length=500)
    description: str = Field(default="", max_length=50000)
    cover_image_url: str = Field(default="", max_length=500)
    audio_url: str = Field(default="", max_length=500)
    subtitle_url: str = Field(default="", max_length=500)
    difficulty_code: str = Field(default="", max_length=50)
    duration_seconds: int = Field(default=0, ge=0, le=86400)
    episode_number: int = Field(default=0, ge=0, le=100000)
    speaker: str = Field(default="", max_length=200)
    sort_order: int = 0
    is_published: Literal[0, 1] = 1
    requires_membership: Literal[0, 1] = 0


class PublicationInput(Input):
    is_published: Literal[0, 1]


class TopicCourseOrderInput(Input):
    """The complete course order for one learning topic."""

    course_ids: list[int] = Field(default_factory=list, max_length=500)


class TopicCourseAssociationInput(Input):
    """Existing courses to associate with a learning topic."""

    course_ids: list[int] = Field(default_factory=list, max_length=500)


class LearningCourseInput(Input):
    # Kept temporarily for API callers saved before topic-course mapping.
    # New callers associate a course from topic maintenance instead.
    topic_id: int | None = Field(default=None, gt=0)
    # material_id remains accepted for callers saved before the course-material
    # mapping was introduced.  New callers should send material_ids.
    material_id: int | None = Field(default=None, gt=0)
    material_ids: list[int] = Field(default_factory=list, max_length=500)
    course_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,119}$")
    title: str = Field(min_length=1, max_length=255)
    title_en: str = Field(default="", max_length=255)
    summary: str = Field(default="", max_length=50000)
    course_type: str = Field(default="lesson", min_length=1, max_length=50)
    content_resource: str = Field(default="", max_length=80)
    content_reference_id: int | None = Field(default=None, gt=0)
    content: dict[str, Any] | list[Any] | None = None
    cover_url: str = Field(default="", max_length=500)
    estimated_minutes: int | None = Field(default=None, ge=1, le=1440)
    difficulty_code: str = Field(default="", max_length=50)
    sort_order: int = 0
    is_published: Literal[0, 1] = 1
    access_policy: Literal["free", "benefit"] = "free"

    @field_validator("material_ids")
    @classmethod
    def valid_material_ids(cls, value):
        if any(material_id <= 0 for material_id in value):
            raise ValueError("material_ids must contain positive material IDs.")
        if len(value) != len(set(value)):
            raise ValueError("material_ids must not contain duplicate materials.")
        return value


class LearningTemplateInput(Input):
    template_code: str = Field(pattern=r"^[a-z][a-z0-9-]{0,79}$")
    template_version: int = Field(default=1, ge=1, le=1000)
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=50000)
    content_kind: Literal["courseware", "dialogue", "structured", "source"] = "source"
    supported_clients: list[Literal["web", "mini", "android", "ios"]] = Field(
        default_factory=lambda: ["web", "mini", "android"], min_length=1, max_length=4
    )
    config: dict[str, Any] | None = None
    status: Literal["active", "inactive"] = "active"
    sort_order: int = 0

    @field_validator("supported_clients")
    @classmethod
    def unique_supported_clients(cls, value):
        if len(value) != len(set(value)):
            raise ValueError("supported_clients must not contain duplicate clients.")
        return value


class LearningMaterialInput(Input):
    # Kept temporarily for API callers saved before the course-material
    # migration. It is ignored on write: materials are linked to topics
    # exclusively through courses.
    topic_id: int | None = Field(default=None, gt=0)
    template_id: int | None = Field(default=None, gt=0)
    material_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,119}$")
    title: str = Field(min_length=1, max_length=255)
    title_en: str = Field(default="", max_length=255)
    summary: str = Field(default="", max_length=50000)
    material_type: str = Field(min_length=1, max_length=50)
    publisher: str = Field(default="", max_length=200)
    version_name: str = Field(default="", max_length=100)
    cover_url: str = Field(default="", max_length=500)
    difficulty_code: str = Field(default="", max_length=50)
    estimated_minutes: int | None = Field(default=None, ge=1, le=100000)
    sort_order: int = 0
    is_published: Literal[0, 1] = 1

    @field_validator("material_code", mode="before")
    @classmethod
    def normalise_material_code(cls, value):
        return value.lower() if isinstance(value, str) else value


class LearningLessonItemInput(Input):
    item_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,119}$")
    item_order: int = 0
    title: str = Field(default="", max_length=255)
    payload: dict[str, Any]
    status: Literal["draft", "published", "archived"] = "draft"


class LearningLessonSectionInput(Input):
    section_code: Literal[
        "core_vocabulary",
        "situational_dialogues",
        "key_sentence_patterns",
        "speaking_practice",
        "mini_exercises",
        "useful_tips",
        "extended_reading",
    ]
    title: str = Field(min_length=1, max_length=150)
    title_en: str = Field(min_length=1, max_length=150)
    sort_order: int = 0
    status: Literal["draft", "published", "archived"] = "draft"
    items: list[LearningLessonItemInput] = Field(default_factory=list, max_length=200)


class LearningLessonSectionsInput(Input):
    sections: list[LearningLessonSectionInput] = Field(min_length=1, max_length=7)


class LearningMaterialLessonInput(Input):
    lesson_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,119}$")
    title: str = Field(min_length=1, max_length=255)
    title_en: str = Field(default="", max_length=255)
    summary: str = Field(default="", max_length=50000)
    illustration_url: str = Field(default="", max_length=500)
    source_resource: str = Field(default="", max_length=80)
    source_reference_id: int | None = Field(default=None, gt=0)
    content: dict[str, Any] | list[Any] | None = None
    lesson_format: Literal["source", "structured", "courseware"] = "source"
    estimated_minutes: int | None = Field(default=None, ge=1, le=1440)
    sort_order: int = 0
    is_published: Literal[0, 1] | None = None
    sections: list[LearningLessonSectionInput] | None = None


class CoursewareBlockInput(Input):
    block_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,119}$")
    block_type: Literal[
        "hero",
        "usage_group",
        "dialogue",
        "comparison",
        "output",
        "recap",
        "wordly_wise_meaning_match",
        "wordly_wise_connections",
        "wordly_wise_application",
        "wordly_wise_reading",
        "wordly_wise_comprehension",
        "wordly_wise_extension",
        "wordly_wise_review",
    ]
    title: str = Field(default="", max_length=255)
    payload: dict[str, Any]
    sort_order: int = 0
    status: Literal["draft", "published", "archived"] = "draft"


class CoursewareBlockSourceInput(Input):
    source_resource: Literal["english_note_item", "english_textbook_sentence"]
    source_reference_id: int = Field(gt=0)
    source_field: Literal[
        "raw_text",
        "english_text",
        "chinese_text",
        "explanation",
        "examples",
    ]
    source_locator: dict[str, Any] | list[Any] | None = None
    source_snapshot_text: str = Field(min_length=1, max_length=50000)
    sort_order: int = 0


class CoursewareBlockSourcesInput(Input):
    items: list[CoursewareBlockSourceInput] = Field(min_length=1, max_length=200)


class NoteCoursewarePreviewInput(Input):
    note_item_id: int = Field(gt=0)


class NoteCoursewareGenerateInput(NoteCoursewarePreviewInput):
    topic_id: int = Field(gt=0)
    material_id: int | None = Field(default=None, gt=0)


class MembershipPlanInput(Input):
    plan_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,63}$")
    name: str = Field(min_length=1, max_length=100)
    name_en: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=500)
    tier_rank: int = Field(default=0, ge=0, le=32767)
    billing_cycle: Literal["free", "manual", "monthly", "quarterly", "yearly", "lifetime"] = "manual"
    duration_days: int | None = Field(default=None, ge=1, le=36500)
    price: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    currency: str = Field(default="CNY", pattern=r"^[A-Z]{3}$")
    icon: str = Field(default="", max_length=32)
    badge_text: str = Field(default="", max_length=50)
    sort_order: int = 0
    status: Literal["draft", "active", "inactive", "archived"] = "draft"
    is_default: bool = False


class MembershipBenefitInput(Input):
    benefit_code: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,79}$")
    name: str = Field(min_length=1, max_length=100)
    name_en: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=500)
    benefit_type: Literal["content_access", "feature_access", "quota", "discount", "service"]
    value_type: Literal["boolean", "integer", "decimal", "string", "json"]
    unit: str = Field(default="", max_length=50)
    scope: Any | None = None
    default_value: Any | None = None
    icon: str = Field(default="", max_length=32)
    sort_order: int = 0
    status: Literal["active", "inactive", "archived"] = "active"


class MembershipPlanBenefitItem(Input):
    benefit_id: int = Field(gt=0)
    grant_value: Any | None = None
    is_enabled: bool = True
    sort_order: int = 0


class MembershipPlanBenefitsInput(Input):
    items: list[MembershipPlanBenefitItem] = Field(default_factory=list, max_length=500)


class MembershipBenefitCourseItem(Input):
    course_id: int = Field(gt=0)
    access_action: Literal["study", "download"] = "study"
    is_enabled: bool = True
    sort_order: int = 0


class MembershipBenefitCoursesInput(Input):
    items: list[MembershipBenefitCourseItem] = Field(default_factory=list, max_length=500)


class UserMembershipInput(Input):
    membership_plan_id: int = Field(gt=0)
    status: Literal["pending", "active", "expired", "cancelled", "revoked"] = "active"
    source: Literal["manual", "purchase", "trial", "gift", "migration", "signup"] = "manual"
    starts_at: datetime
    ends_at: datetime | None = None
    auto_renew: bool = False
    external_reference: str = Field(default="", max_length=100)
    cancelled_at: datetime | None = None
    cancel_reason: str = Field(default="", max_length=500)


class LearningUserCourseInput(Input):
    course_id: int = Field(gt=0)
    status: Literal["active", "archived"] = "active"


class LearningProgressItemInput(Input):
    item_key: str = Field(min_length=1, max_length=160)
    item_type: str = Field(default="course_item", min_length=1, max_length=50)
    item_reference_id: int | None = Field(default=None, gt=0)
    is_completed: bool = False
    last_position_seconds: int = Field(default=0, ge=0, le=604800)
    score: int | None = Field(default=None, ge=0, le=100)


class LearningCourseProgressInput(Input):
    course_id: int = Field(gt=0)
    total_item_count: int | None = Field(default=None, ge=0, le=100000)
    last_item_key: str | None = Field(default=None, min_length=1, max_length=160)
    last_item_id: int | None = Field(default=None, gt=0)
    last_position_seconds: int | None = Field(default=None, ge=0, le=604800)
    item: LearningProgressItemInput | None = None
    completed: bool | None = None


class LearningStudySessionStartInput(Input):
    course_id: int = Field(gt=0)
    platform: Literal["web", "mini_program", "android", "ios"] = "web"
    entry_source: str = Field(default="", max_length=100)


class LearningStudySessionFinishInput(Input):
    active_seconds: int | None = Field(default=None, ge=0, le=86400)


def _valid_json_object(value: dict[str, Any], *, field_name: str, max_bytes: int = 20_000):
    try:
        encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} must contain JSON-compatible values.") from error
    if len(encoded.encode("utf-8")) > max_bytes:
        raise ValueError(f"{field_name} is too large.")
    return value


class AppPresentationConfigInput(Input):
    target_type: Literal["module", "topic", "course", "material", "collection", "placement"]
    target_key: str = Field(pattern=r"^[a-z0-9][a-z0-9._:-]{0,119}$")
    platform: Literal["all", "android", "ios", "web", "mini"] = "all"
    layout_code: str = Field(pattern=r"^[a-z][a-z0-9_]{0,79}$")
    presentation: dict[str, Any] = Field(default_factory=dict)
    min_app_version: str = Field(default="", max_length=40)
    fallback_action: dict[str, Any] | None = None
    status: Literal["active", "inactive"] = "active"
    sort_order: int = 0

    @field_validator("presentation")
    @classmethod
    def valid_presentation(cls, value):
        return _valid_json_object(value, field_name="presentation")

    @field_validator("fallback_action")
    @classmethod
    def valid_fallback_action(cls, value):
        if value is None:
            return None
        return _valid_json_object(value, field_name="fallback_action", max_bytes=4_000)


_ANALYTICS_EVENT_NAME_PATTERN = r"^[a-z][a-z0-9_]{0,79}$"
_ANALYTICS_PROPERTY_NAME_PATTERN = r"^[a-z][a-z0-9_]{0,79}$"
_ANALYTICS_SENSITIVE_PROPERTY_NAMES = frozenset(
    {
        "password",
        "secret",
        "token",
        "authorization",
        "cookie",
        "csrf",
        "email",
        "phone",
        "address",
        "invite_code",
        "audio_data",
        "raw_audio",
        "note_text",
        "raw_text",
        "content",
    }
)


def _valid_analytics_properties(value: dict[str, Any]):
    if len(value) > 20:
        raise ValueError("properties may contain at most 20 values.")
    for key, item in value.items():
        if not isinstance(key, str) or not re.fullmatch(_ANALYTICS_PROPERTY_NAME_PATTERN, key):
            raise ValueError("analytics property names must use lowercase snake_case.")
        if key in _ANALYTICS_SENSITIVE_PROPERTY_NAMES:
            raise ValueError("analytics properties must not contain personal or learning content.")
        if isinstance(item, str):
            if len(item) > 500:
                raise ValueError("analytics property text is too long.")
        elif isinstance(item, bool) or item is None or isinstance(item, int):
            continue
        elif isinstance(item, float):
            if not math.isfinite(item):
                raise ValueError("analytics property numbers must be finite.")
        else:
            raise ValueError("analytics properties only support scalar values.")
    return value


class AnalyticsSubjectInput(Input):
    subject_type: str = Field(pattern=r"^[a-z][a-z0-9_-]{0,49}$")
    subject_key: str = Field(min_length=1, max_length=500)


class AnalyticsSourceInput(Input):
    screen: str = Field(default="", pattern=r"^[a-z0-9._-]{0,79}$")
    placement: str = Field(default="", pattern=r"^[a-z0-9._-]{0,119}$")
    item_key: str = Field(default="", max_length=500)


class AnalyticsContextInput(Input):
    platform: Literal["android", "ios", "web", "mini"]
    app_version: str = Field(min_length=1, max_length=40)
    bootstrap_revision: str = Field(default="", max_length=80)
    renderer: str = Field(default="", pattern=r"^[a-z0-9._-]{0,79}$")


class AnalyticsEventInput(Input):
    event_id: UUID
    event_name: str = Field(pattern=_ANALYTICS_EVENT_NAME_PATTERN)
    occurred_at: datetime
    session_id: str = Field(default="", max_length=120)
    subject: AnalyticsSubjectInput | None = None
    source: AnalyticsSourceInput | None = None
    context: AnalyticsContextInput
    properties: dict[str, Any] = Field(default_factory=dict)

    @field_validator("properties")
    @classmethod
    def valid_properties(cls, value):
        return _valid_analytics_properties(value)


class AnalyticsEventBatchInput(Input):
    events: list[AnalyticsEventInput] = Field(min_length=1, max_length=100)

    @field_validator("events")
    @classmethod
    def unique_event_ids(cls, value):
        event_ids = [event.event_id for event in value]
        if len(event_ids) != len(set(event_ids)):
            raise ValueError("events must not contain duplicate event_id values.")
        return value


class AnalyticsEventDefinitionInput(Input):
    event_name: str = Field(pattern=_ANALYTICS_EVENT_NAME_PATTERN)
    description: str = Field(default="", max_length=500)
    allowed_properties: list[str] = Field(default_factory=list, max_length=20)
    sample_rate: int = Field(default=100, ge=0, le=100)
    status: Literal["active", "inactive"] = "active"

    @field_validator("allowed_properties")
    @classmethod
    def valid_allowed_properties(cls, value):
        if len(value) != len(set(value)):
            raise ValueError("allowed_properties must not contain duplicate values.")
        _valid_analytics_properties({key: "value" for key in value})
        return value
