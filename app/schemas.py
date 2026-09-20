from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Role = Literal["user", "learner", "premium_learner", "volunteer", "leader", "admin"]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=72)


class ProfileInput(Input):
    full_name: str = Field(min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=150)
    contact_number: str | None = Field(default=None, max_length=30)
    home_address: str | None = Field(default=None, max_length=255)

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
    example_image_url: str = Field(default="", max_length=500)
    example_image_alt: str = Field(default="", max_length=255)
    keywords: str = Field(default="", max_length=500)
    share_status: Literal[0, 1] = 0
    priority_order: int = 0

    @field_validator("example_image_url")
    @classmethod
    def valid_image_url(cls, value):
        if value and not value.startswith(("https://", "http://", "/static/")):
            raise ValueError("Use an HTTP(S) image URL or an uploaded /static/ image.")
        return value


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
