"""Registry proving that every mapped table has a corresponding service."""

from app.services.accounts import LoginAuditService, UserService
from app.services.content import CONTENT_TABLE_SERVICE_TYPES
from app.services.courseware import COURSEWARE_TABLE_SERVICE_TYPES
from app.services.learning_catalog import LEARNING_CATALOG_TABLE_SERVICE_TYPES
from app.services.learning_progress import LEARNING_PROGRESS_TABLE_SERVICE_TYPES
from app.services.lesson_content import LESSON_CONTENT_TABLE_SERVICE_TYPES
from app.services.membership import MEMBERSHIP_TABLE_SERVICE_TYPES
from app.services.progress import StudyProgressService

TABLE_SERVICE_TYPES = {
    **CONTENT_TABLE_SERVICE_TYPES,
    **COURSEWARE_TABLE_SERVICE_TYPES,
    **LEARNING_CATALOG_TABLE_SERVICE_TYPES,
    **LEARNING_PROGRESS_TABLE_SERVICE_TYPES,
    **LESSON_CONTENT_TABLE_SERVICE_TYPES,
    **MEMBERSHIP_TABLE_SERVICE_TYPES,
    "user": UserService,
    "login_audit": LoginAuditService,
    "study_progress": StudyProgressService,
}
