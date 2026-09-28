"""Architecture contract: every mapped table has a DAO and service registration."""

from app import models as m
from app.dao import TABLE_DAO_TYPES
from app.services.registry import TABLE_SERVICE_TYPES


def test_every_mapped_table_has_a_dao_and_service():
    table_names = set(m.metadata.tables)
    assert set(TABLE_DAO_TYPES) == table_names
    assert set(TABLE_SERVICE_TYPES) == table_names
    assert {table_name: dao_type.table.name for table_name, dao_type in TABLE_DAO_TYPES.items()} == {
        table_name: table_name for table_name in table_names
    }
