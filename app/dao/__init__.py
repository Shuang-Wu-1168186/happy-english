"""Data access objects, one registered DAO for every mapped database table."""

from app.dao.accounts import ACCOUNT_TABLE_DAO_TYPES
from app.dao.content import CONTENT_TABLE_DAO_TYPES
from app.dao.courseware import COURSEWARE_TABLE_DAO_TYPES
from app.dao.learning_catalog import LEARNING_CATALOG_TABLE_DAO_TYPES
from app.dao.learning_progress import LEARNING_PROGRESS_TABLE_DAO_TYPES
from app.dao.membership import MEMBERSHIP_TABLE_DAO_TYPES
from app.dao.progress import STUDY_PROGRESS_TABLE_DAO_TYPES

TABLE_DAO_TYPES = {
    **ACCOUNT_TABLE_DAO_TYPES,
    **CONTENT_TABLE_DAO_TYPES,
    **COURSEWARE_TABLE_DAO_TYPES,
    **LEARNING_CATALOG_TABLE_DAO_TYPES,
    **LEARNING_PROGRESS_TABLE_DAO_TYPES,
    **MEMBERSHIP_TABLE_DAO_TYPES,
    **STUDY_PROGRESS_TABLE_DAO_TYPES,
}
