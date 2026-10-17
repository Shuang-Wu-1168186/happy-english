from scripts import export_aliyun_learning_catalog as exporter


def test_textbook_release_aligns_target_lesson_codes_before_upsert():
    lines: list[str] = []

    exporter.emit_target_upserts(
        lines,
        scoped=True,
        replace_relationships=False,
    )

    sql = "\n".join(lines)
    alignment = "UPDATE `learning_material_lesson` AS `target_lesson`"
    upsert = "INSERT INTO `learning_material_lesson`"

    assert alignment in sql
    assert "JOIN `english_textbook_lesson` AS `target_source`" in sql
    assert "`source`.`textbook_unit_name` = `target_source`.`unit_name`" in sql
    assert "`source`.`textbook_lesson_name` = `target_source`.`lesson_name`" in sql
    assert "SET `target_lesson`.`lesson_code` = `source`.`lesson_code`" in sql
    assert sql.index(alignment) < sql.index(upsert)
