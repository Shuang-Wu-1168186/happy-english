"""Application services for the module → topic → material → course catalogue."""

import json

from fastapi import HTTPException
from sqlalchemy import func, or_, select

from app import models as m
from app import schemas as s
from app.dao.learning_catalog import (
    LearningCourseDAO,
    LearningCourseMaterialDAO,
    LearningMaterialDAO,
    LearningMaterialLessonDAO,
    LearningModuleDAO,
    LearningTemplateDAO,
    LearningTopicCourseDAO,
    LearningTopicDAO,
)


# This is the cross-client renderer contract.  The same `code` and `version`
# are registered by the web application and the mini program.  The database
# may control naming, ordering, and activation, but it cannot point a material
# at an arbitrary renderer that one of the clients does not ship.
MATERIAL_TEMPLATE_DEFINITIONS = {
    "standard": {
        "version": 1,
        "name": "通用课时",
        "description": "适合句子、笔记和自包含内容的通用学习页。",
        "content_kind": "source",
        "source_resources": None,
    },
    "put-aside": {
        "version": 1,
        "name": "Put aside 课件",
        "description": "按短语、用法、情景和输出区块组织的课件。",
        "content_kind": "courseware",
        "source_resources": (),
    },
    "dialogue": {
        "version": 1,
        "name": "情景对话",
        "description": "按词汇、对话和练习分区展示的口语对话页。",
        "content_kind": "dialogue",
        "source_resources": ("dialogues",),
    },
    "textbook": {
        "version": 1,
        "name": "课本课文",
        "description": "按单元、课文和中英对照展示的教材页。",
        "content_kind": "source",
        "source_resources": ("textbook",),
    },
    "cards": {
        "version": 1,
        "name": "单词卡片",
        "description": "适合儿童卡片、数学卡片和词汇卡片的学习页。",
        "content_kind": "source",
        "source_resources": ("kids-cards", "math-cards", "vocabulary"),
    },
    "phonics": {
        "version": 1,
        "name": "自然拼读",
        "description": "按音素、示例和小测展示的拼读学习页。",
        "content_kind": "source",
        "source_resources": ("phonics",),
    },
    "interview": {
        "version": 1,
        "name": "面试练习",
        "description": "按面试问题、答案和要点展示的练习页。",
        "content_kind": "source",
        "source_resources": ("interviews",),
    },
}

DEFAULT_TEMPLATE_BY_MATERIAL_TYPE = {
    "courseware": "put-aside",
    "dialogue": "dialogue",
    "textbook": "textbook",
    "card_set": "cards",
    "phonics": "phonics",
    "interview": "interview",
    "exam": "interview",
}


def serialise_catalog(row):
    """Return a catalogue row with optional JSON payloads decoded."""
    result = dict(row)
    for json_field, output_field, fallback in (
        ("content_json", "content", None),
        ("config_json", "config", None),
        ("supported_clients_json", "supported_clients", []),
    ):
        encoded = result.pop(json_field, None)
        if encoded is not None:
            try:
                result[output_field] = json.loads(encoded)
            except (TypeError, ValueError):
                result[output_field] = fallback
    return result


def serialise_template(row):
    """Expose a template as a versioned client renderer contract."""
    result = serialise_catalog(row)
    code = result.get("template_code") or result.get("code") or "standard"
    version = int(result.get("template_version") or result.get("version") or 1)
    clients = result.get("supported_clients")
    if not isinstance(clients, list):
        clients = []
    config = result.get("config")
    return {
        **result,
        "code": code,
        "version": version,
        "renderer": f"{code}.v{version}",
        "supported_clients": clients,
        "config": config if isinstance(config, dict) else {},
    }


class LearningCatalogTableService:
    """Table-level rules shared by every learning catalogue service."""

    dao_type = None

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def require_any(self, item_id):
        row = self.dao.find_by_id(item_id)
        if not row:
            raise HTTPException(404, "Learning catalogue record not found.")
        return row

    def require_public(self, item_id):
        row = self.dao.get_published(item_id)
        if not row:
            raise HTTPException(404, "Learning catalogue record not found.")
        return row

    def list_all(self, *conditions):
        return [
            serialise_catalog(row) for row in self.dao.list_where(*conditions, order_by=self.dao.ordering())
        ]

    def save(self, item_id, values, actor):
        if item_id is None:
            values["created_by"] = actor["id"]
            item_id = self.dao.insert(values)
        else:
            self.require_any(item_id)
            values["updated_by"] = actor["id"]
            self.dao.update(item_id, values)
        return self.require_any(item_id)

    def delete(self, item_id):
        self.require_any(item_id)
        self.dao.delete(item_id)


class LearningModuleService(LearningCatalogTableService):
    dao_type = LearningModuleDAO

    def list_public(self):
        return [serialise_catalog(row) for row in self.dao.list_modules()]


class LearningTopicService(LearningCatalogTableService):
    dao_type = LearningTopicDAO

    def list_public(self, module_id=None):
        return [serialise_catalog(row) for row in self.dao.list_topics(module_id)]


class LearningTemplateService:
    """Template records are an allowlisted contract, not executable content."""

    dao_type = LearningTemplateDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def require_any(self, template_id):
        row = self.dao.find_by_id(template_id)
        if not row:
            raise HTTPException(404, "Learning template not found.")
        return row

    def require_active(self, template_id):
        row = self.require_any(template_id)
        if row["status"] != "active":
            raise HTTPException(422, "The selected learning template is inactive.")
        return row

    def list_all(self, active_only=False):
        rows = self.dao.list_active() if active_only else self.dao.list_where(
            order_by=self.dao.ordering()
        )
        return [serialise_template(row) for row in rows]


class LearningMaterialService(LearningCatalogTableService):
    dao_type = LearningMaterialDAO

    def list_public(self, topic_id=None):
        return [serialise_catalog(row) for row in self.dao.list_materials(topic_id)]


class LearningMaterialLessonService(LearningCatalogTableService):
    dao_type = LearningMaterialLessonDAO

    def list_public(self, material_id=None):
        return [serialise_catalog(row) for row in self.dao.list_lessons(material_id)]


class LearningCourseService(LearningCatalogTableService):
    dao_type = LearningCourseDAO

    def list_public(self):
        return [serialise_catalog(row) for row in self.dao.list_courses()]


class LearningCourseMaterialService:
    """Ordered material mappings owned by a course."""

    dao_type = LearningCourseMaterialDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class LearningTopicCourseService:
    dao_type = LearningTopicCourseDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


LEARNING_CATALOG_TABLE_SERVICE_TYPES = {
    "learning_module": LearningModuleService,
    "learning_topic": LearningTopicService,
    "learning_template": LearningTemplateService,
    "learning_material": LearningMaterialService,
    "learning_material_lesson": LearningMaterialLessonService,
    "learning_course": LearningCourseService,
    "learning_topic_course": LearningTopicCourseService,
    "learning_course_material": LearningCourseMaterialService,
}


class LearningCatalogService:
    """Cross-table business rules and public hierarchy responses."""

    def __init__(self, db):
        self.db = db
        self.modules = LearningModuleService(db)
        self.topics = LearningTopicService(db)
        self.templates = LearningTemplateService(db)
        self.materials = LearningMaterialService(db)
        self.material_lessons = LearningMaterialLessonService(db)
        self.courses = LearningCourseService(db)
        self.topic_courses = LearningTopicCourseService(db)
        self.course_materials = LearningCourseMaterialService(db)
        self._template_cache = {}

    @staticmethod
    def _none_when_blank(values, fields):
        for field in fields:
            if values.get(field) == "":
                values[field] = None
        return values

    @staticmethod
    def _encode_json(value, field_name):
        if value is None:
            return None
        try:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError) as error:
            raise HTTPException(422, f"{field_name} must be valid JSON data.") from error

    @staticmethod
    def _default_template_code(material_type):
        return DEFAULT_TEMPLATE_BY_MATERIAL_TYPE.get(material_type, "standard")

    def _fallback_template(self, material_type):
        code = self._default_template_code(material_type)
        definition = MATERIAL_TEMPLATE_DEFINITIONS[code]
        return {
            "id": None,
            "template_code": code,
            "template_version": definition["version"],
            "code": code,
            "version": definition["version"],
            "renderer": f"{code}.v{definition['version']}",
            "name": definition["name"],
            "description": definition["description"],
            "content_kind": definition["content_kind"],
            "supported_clients": ["web", "mini"],
            "config": {},
            "status": "active",
            "sort_order": 0,
            "is_fallback": True,
        }

    def _template_for_material(self, material, require_active=False):
        template_id = material.get("template_id") if hasattr(material, "get") else None
        if template_id:
            template = self._template_cache.get(template_id)
            if template is None:
                template = self.templates.require_any(template_id)
                self._template_cache[template_id] = template
            if require_active and template["status"] != "active":
                raise HTTPException(422, "The selected learning template is inactive.")
            return serialise_template(template)
        material_type = material.get("material_type") if hasattr(material, "get") else ""
        return self._fallback_template(material_type)

    def _material_view(self, material):
        result = serialise_catalog(material)
        result["template"] = self._template_for_material(material)
        return result

    def _template_record_values(self, payload: s.LearningTemplateInput):
        values = self._none_when_blank(payload.model_dump(), ("description",))
        config = values.pop("config")
        clients = values.pop("supported_clients")
        definition = MATERIAL_TEMPLATE_DEFINITIONS.get(values["template_code"])
        if not definition or values["template_version"] != definition["version"]:
            raise HTTPException(
                422,
                "模板编号或版本未在 Web 和小程序的渲染器注册，不能保存。",
            )
        if values["content_kind"] != definition["content_kind"]:
            raise HTTPException(422, "模板内容类型必须与客户端渲染器定义一致。")
        if set(clients) != {"web", "mini"}:
            raise HTTPException(422, "教材模板必须同时注册 Web 和小程序渲染器。")
        values["config_json"] = self._encode_json(config or {}, "config")
        values["supported_clients_json"] = self._encode_json(clients, "supported_clients")
        return values

    def _default_template_id(self, material_type):
        code = self._default_template_code(material_type)
        row = self.db.execute(
            select(m.learning_template.c.id).where(
                m.learning_template.c.template_code == code,
                m.learning_template.c.template_version
                == MATERIAL_TEMPLATE_DEFINITIONS[code]["version"],
                m.learning_template.c.status == "active",
            )
        ).first()
        return row[0] if row else None

    def _validate_template_material_compatibility(self, material, template=None):
        template = template or self._template_for_material(material)
        # Test fixtures and pre-migration rows can be read through the default
        # renderer without pretending that they are already bound records.
        if template.get("is_fallback"):
            return
        code = template["code"]
        definition = MATERIAL_TEMPLATE_DEFINITIONS.get(code)
        if not definition or template["version"] != definition["version"]:
            raise HTTPException(422, "教材使用了未注册的模板编号或版本。")
        resources = definition["source_resources"]
        for lesson in self.material_lessons.dao.list_where(
            self.material_lessons.dao.table.c.material_id == material["id"],
            order_by=self.material_lessons.dao.ordering(),
        ):
            self._validate_lesson_template_compatibility(lesson, template)

    def _validate_lesson_template_compatibility(self, lesson, template):
        if template.get("is_fallback"):
            return
        code = template["code"]
        definition = MATERIAL_TEMPLATE_DEFINITIONS.get(code)
        if not definition or template["version"] != definition["version"]:
            raise HTTPException(422, "教材使用了未注册的模板编号或版本。")
        if code == "put-aside":
            if lesson["lesson_format"] != "courseware":
                raise HTTPException(422, "Put aside 模板只能包含课件区块课时。")
            return
        if lesson["lesson_format"] == "courseware":
            raise HTTPException(422, "当前教材模板不能包含课件区块课时，请选择 Put aside 模板。")
        allowed_resources = definition["source_resources"]
        source_resource = lesson.get("source_resource") if hasattr(lesson, "get") else None
        if allowed_resources is not None and source_resource not in allowed_resources:
            raise HTTPException(
                422,
                f"{template['name']} 模板不支持来源“{source_resource or '自包含内容'}”。",
            )

    def list_modules(self):
        return {"items": self.modules.list_public()}

    def _public_topics(self):
        rows = (
            self.db.execute(
                select(m.learning_topic)
                .join(
                    m.learning_module,
                    m.learning_module.c.id == m.learning_topic.c.module_id,
                )
                .where(
                    m.learning_topic.c.is_published == 1,
                    m.learning_module.c.is_published == 1,
                )
                .order_by(m.learning_topic.c.sort_order, m.learning_topic.c.id)
            )
            .mappings()
            .all()
        )
        return [serialise_catalog(row) for row in rows]

    def _public_materials(self):
        rows = (
            self.db.execute(
                select(m.learning_material)
                .join(
                    m.learning_topic,
                    m.learning_topic.c.id == m.learning_material.c.topic_id,
                )
                .join(
                    m.learning_module,
                    m.learning_module.c.id == m.learning_topic.c.module_id,
                )
                .where(
                    m.learning_material.c.is_published == 1,
                    m.learning_topic.c.is_published == 1,
                    m.learning_module.c.is_published == 1,
                )
                .order_by(m.learning_material.c.sort_order, m.learning_material.c.id)
            )
            .mappings()
            .all()
        )
        return [self._material_view(row) for row in rows]

    def _public_courses(self):
        rows = (
            self.db.execute(
                select(m.learning_course)
                .join(
                    m.learning_topic_course,
                    m.learning_topic_course.c.course_id == m.learning_course.c.id,
                )
                .join(
                    m.learning_topic,
                    m.learning_topic.c.id == m.learning_topic_course.c.topic_id,
                )
                .join(
                    m.learning_module,
                    m.learning_module.c.id == m.learning_topic.c.module_id,
                )
                .where(
                    m.learning_course.c.is_published == 1,
                    m.learning_topic.c.is_published == 1,
                    m.learning_module.c.is_published == 1,
                )
                .distinct()
                .order_by(m.learning_course.c.sort_order, m.learning_course.c.id)
            )
            .mappings()
            .all()
        )
        return [
            self.course_summary(row, published_only=True)
            for row in rows
            if self._course_materials_are_public(row)
        ]

    def _courses_for_topic(self, topic_id, published_only=False):
        conditions = [m.learning_topic_course.c.topic_id == topic_id]
        if published_only:
            conditions.append(m.learning_course.c.is_published == 1)
        return self.db.execute(
            select(
                m.learning_course,
                m.learning_topic_course.c.sort_order.label("topic_course_sort_order"),
            )
            .join(
                m.learning_topic_course,
                m.learning_topic_course.c.course_id == m.learning_course.c.id,
            )
            .where(*conditions)
            .order_by(
                m.learning_topic_course.c.sort_order,
                m.learning_topic_course.c.id,
            )
        ).mappings().all()

    def _course_topic_rows(self, course_id, published_only=False):
        conditions = [m.learning_topic_course.c.course_id == course_id]
        if published_only:
            conditions.extend(
                [
                    m.learning_topic.c.is_published == 1,
                    m.learning_module.c.is_published == 1,
                ]
            )
        statement = (
            select(
                m.learning_topic,
                m.learning_topic_course.c.sort_order.label("course_topic_sort_order"),
            )
            .join(
                m.learning_topic_course,
                m.learning_topic_course.c.topic_id == m.learning_topic.c.id,
            )
            .where(*conditions)
            .order_by(
                m.learning_topic_course.c.sort_order,
                m.learning_topic_course.c.id,
            )
        )
        if published_only:
            statement = statement.join(
                m.learning_module,
                m.learning_module.c.id == m.learning_topic.c.module_id,
            )
        return self.db.execute(statement).mappings().all()

    def _course_material_rows(self, course, published_only=False):
        """Return a course's materials in course order.

        A one-time fallback reads the old `learning_course.material_id` field
        for an application node that is deployed before its database migration.
        Once a mapping exists, it is always the source of truth.
        """
        course_id = course["id"] if hasattr(course, "get") else course
        rows = self.db.execute(
            select(
                m.learning_material,
                m.learning_course_material.c.sort_order.label("course_material_sort_order"),
            )
            .join(
                m.learning_course_material,
                m.learning_course_material.c.material_id == m.learning_material.c.id,
            )
            .where(m.learning_course_material.c.course_id == course_id)
            .order_by(
                m.learning_course_material.c.sort_order,
                m.learning_course_material.c.id,
            )
        ).mappings().all()
        if published_only:
            rows = [row for row in rows if row["is_published"] == 1]
        legacy_material_id = course.get("material_id") if hasattr(course, "get") else None
        if rows or legacy_material_id is None:
            return rows

        legacy = (
            self.materials.dao.get_published(legacy_material_id)
            if published_only
            else self.materials.dao.find_by_id(legacy_material_id)
        )
        if not legacy:
            return []
        return [{**dict(legacy), "course_material_sort_order": 0}]

    def _course_material_summaries(self, course, published_only=False):
        summaries = []
        for row in self._course_material_rows(course, published_only):
            material = self._material_view(row)
            material["course_sort_order"] = material.pop("course_material_sort_order", 0)
            summaries.append(material)
        return summaries

    def _public_materials_for_topic(self, topic_id):
        """Return materials exposed by the topic's associated courses."""
        materials = []
        seen_ids = set()
        for course in self._courses_for_topic(topic_id, published_only=True):
            if not self._course_materials_are_public(course):
                continue
            for material in self._course_material_summaries(course, published_only=True):
                if material["id"] in seen_ids:
                    continue
                seen_ids.add(material["id"])
                materials.append(material)
        return materials

    def _course_materials_are_public(self, course):
        """A public course cannot expose a partially unpublished material set."""
        return all(row["is_published"] == 1 for row in self._course_material_rows(course))

    def course_summary(self, course, published_only=False):
        """Serialize a course with its ordered material summaries.

        `material_id` remains in responses as the first material for older
        clients.  New clients use `material_ids` and `materials`.
        """
        result = serialise_catalog(course)
        if "topic_course_sort_order" in result:
            result["sort_order"] = result["topic_course_sort_order"]
        materials = self._course_material_summaries(course, published_only)
        material_ids = [material["id"] for material in materials]
        result["materials"] = materials
        result["material_ids"] = material_ids
        result["material_id"] = material_ids[0] if material_ids else None
        if materials:
            result["material_title"] = materials[0]["title"]
            result["material_title_en"] = materials[0].get("title_en") or ""
            result["material_code"] = materials[0]["material_code"]
            result["material_titles"] = " / ".join(material["title"] for material in materials)
        topics = [
            serialise_catalog(topic)
            for topic in self._course_topic_rows(result["id"], published_only)
        ]
        result["topics"] = topics
        result["topic_ids"] = [topic["id"] for topic in topics]
        return result

    def _courses_for_material(self, material_id):
        mapped_course_ids = select(m.learning_course_material.c.course_id).where(
            m.learning_course_material.c.material_id == material_id
        )
        return self.courses.dao.list_where(
            or_(
                self.courses.dao.table.c.id.in_(mapped_course_ids),
                self.courses.dao.table.c.material_id == material_id,
            ),
            order_by=self.courses.dao.ordering(),
        )

    def _replace_course_materials(self, course_id, material_ids, actor):
        self.course_materials.dao.delete_where(
            self.course_materials.dao.table.c.course_id == course_id
        )
        for position, material_id in enumerate(material_ids, start=1):
            self.course_materials.dao.insert(
                {
                    "course_id": course_id,
                    "material_id": material_id,
                    "sort_order": position * 10,
                    "created_by": actor["id"],
                    "updated_by": actor["id"],
                }
            )

    def get_module(self, module_id):
        result = serialise_catalog(self.modules.require_public(module_id))
        result["topics"] = self.topics.list_public(module_id)
        return result

    def list_topics(self, module_id=None):
        if module_id is not None:
            self.modules.require_public(module_id)
            return {"items": self.topics.list_public(module_id)}
        return {"items": self._public_topics()}

    def get_topic(self, topic_id):
        topic = self.topics.require_public(topic_id)
        self.modules.require_public(topic["module_id"])
        result = serialise_catalog(topic)
        result["courses"] = [
            self.course_summary(course, published_only=True)
            for course in self._courses_for_topic(topic_id, published_only=True)
            if self._course_materials_are_public(course)
        ]
        result["materials"] = self._public_materials_for_topic(topic_id)
        return result

    def list_materials(self, topic_id=None):
        if topic_id is not None:
            topic = self.topics.require_public(topic_id)
            self.modules.require_public(topic["module_id"])
            return {"items": self._public_materials_for_topic(topic_id)}
        return {"items": self._public_materials()}

    def _lesson_views(
        self,
        material_id,
        include_content=False,
        unlocked_lesson_count=None,
    ):
        material = self.materials.require_any(material_id)
        template = self._template_for_material(material)
        rows = self.material_lessons.dao.list_lessons(material_id)
        return [
            self._lesson_view(
                row,
                include_content=include_content,
                is_locked=(unlocked_lesson_count is not None and index >= unlocked_lesson_count),
                template=template,
            )
            for index, row in enumerate(rows)
        ]

    def _lesson_view(self, lesson, include_content=False, is_locked=False, template=None):
        if template is None:
            template = self._template_for_material(
                self.materials.require_any(lesson["material_id"])
            )
        result = serialise_catalog(lesson)
        result["template"] = template
        result["is_locked"] = is_locked
        result["access_state"] = "locked" if is_locked else "available"
        if is_locked:
            # Do not put self-contained JSON or a source record into an
            # otherwise locked lesson response.  The client still receives
            # enough metadata to draw the course catalogue and lock state.
            result.pop("content", None)
            result.pop("source_resource", None)
            result.pop("source_reference_id", None)
            result["lock_reason"] = "membership"
            result["render_payload"] = {
                "template": template,
                "content_kind": template["content_kind"],
                "content": None,
            }
            return result
        if not include_content:
            result.pop("content", None)
            result["render_payload"] = {
                "template": template,
                "content_kind": template["content_kind"],
                "content": None,
            }
            return result
        if lesson["lesson_format"] == "courseware":
            # Courseware has its own editable block model; never fall back to
            # the legacy source/content fields for this lesson format.
            result.pop("content", None)
            from app.services.courseware import CoursewareBlockService

            blocks = CoursewareBlockService(self.db).list_for_lesson(
                lesson["id"], published_only=True
            )
            result["courseware_blocks"] = blocks
            result["render_payload"] = {
                "template": template,
                "content_kind": "courseware",
                "content": {"blocks": blocks},
            }
            return result
        if lesson["source_resource"] and lesson["source_reference_id"]:
            result["source_content"] = self._load_lesson_source(lesson)
        result["render_payload"] = {
            "template": template,
            "content_kind": template["content_kind"],
            "source_resource": result.get("source_resource"),
            "content": result.get("source_content") or result.get("content") or {},
        }
        return result

    def _load_lesson_source(self, lesson):
        source_resource = lesson["source_resource"]
        source_reference_id = lesson["source_reference_id"]
        if source_resource == "notes":
            note = (
                self.db.execute(
                    select(m.english_note).where(
                        m.english_note.c.id == source_reference_id,
                        m.english_note.c.share_status == 1,
                    )
                )
                .mappings()
                .first()
            )
            if not note:
                raise HTTPException(404, "The shared note used by this lesson is unavailable.")
            items = (
                self.db.execute(
                    select(m.english_note_item)
                    .where(
                        m.english_note_item.c.note_id == source_reference_id,
                        m.english_note_item.c.share_status == 1,
                    )
                    .order_by(m.english_note_item.c.priority_order, m.english_note_item.c.id)
                )
                .mappings()
                .all()
            )
            from app.services.content import serialise_content

            return {
                **serialise_content(note),
                "items": [serialise_content(item) for item in items],
            }

        if source_resource == "dialogues":
            root = (
                self.db.execute(
                    select(m.daily_spoken_dialogue_item).where(
                        m.daily_spoken_dialogue_item.c.id == source_reference_id,
                        m.daily_spoken_dialogue_item.c.is_published == 1,
                    )
                )
                .mappings()
                .first()
            )
            if not root:
                raise HTTPException(404, "The dialogue used by this lesson is unavailable.")
            items = (
                self.db.execute(
                    select(m.daily_spoken_dialogue_item)
                    .where(
                        m.daily_spoken_dialogue_item.c.lesson_code == root["lesson_code"],
                        m.daily_spoken_dialogue_item.c.is_published == 1,
                    )
                    .order_by(
                        m.daily_spoken_dialogue_item.c.section_order,
                        m.daily_spoken_dialogue_item.c.item_order,
                        m.daily_spoken_dialogue_item.c.id,
                    )
                )
                .mappings()
                .all()
            )
            from app.services.content import serialise_content

            return {
                "lesson_code": root["lesson_code"],
                "chapter_title": root["chapter_title"],
                "lesson_title": root["lesson_title"],
                "items": [serialise_content(item) for item in items],
            }

        from app.services.content import ContentService

        return ContentService(self.db).get_content(source_resource, source_reference_id)

    def _material_access(self, user, material_id):
        """Resolve course membership rules for the direct material route."""
        if user is None:
            return {
                "access_state": "available",
                "membership_id": None,
                "preview_lesson_count": None,
                "requires_membership": False,
                "unlocked_lesson_indexes": None,
            }
        # Import lazily to keep the catalogue and membership services from
        # importing each other while their modules are initialising.
        from app.services.membership import MembershipService

        return MembershipService(self.db).user_courses.material_access(
            user["id"], material_id
        )

    def get_material(self, material_id, include_lesson_content=False, user=None):
        material = self.materials.require_public(material_id)
        topic = self.topics.require_public(material["topic_id"])
        self.modules.require_public(topic["module_id"])
        result = self._material_view(material)
        template = result["template"]
        access = self._material_access(user, material_id)
        unlocked_indexes = access.pop("unlocked_lesson_indexes", None)
        result.update(access)
        result["lessons"] = [
            self._lesson_view(
                lesson,
                include_content=include_lesson_content,
                is_locked=(
                    unlocked_indexes is not None and index not in unlocked_indexes
                ),
                template=template,
            )
            for index, lesson in enumerate(self.material_lessons.dao.list_lessons(material_id))
        ]
        return result

    def get_material_lesson(self, material_id, lesson_id, user=None):
        material = self.materials.require_public(material_id)
        topic = self.topics.require_public(material["topic_id"])
        self.modules.require_public(topic["module_id"])
        lesson = self.material_lessons.require_any(lesson_id)
        if lesson["material_id"] != material_id or lesson["is_published"] != 1:
            raise HTTPException(404, "Learning material lesson not found.")
        access = self._material_access(user, material_id)
        unlocked_indexes = access.pop("unlocked_lesson_indexes", None)
        lesson_index = next(
            (
                index
                for index, row in enumerate(self.material_lessons.dao.list_lessons(material_id))
                if row["id"] == lesson_id
            ),
            None,
        )
        is_locked = (
            unlocked_indexes is not None
            and lesson_index not in unlocked_indexes
        )
        if is_locked:
            raise HTTPException(403, "该章节需要会员解锁，请升级会员后继续学习。")
        return self._lesson_view(
            lesson,
            include_content=True,
            template=self._template_for_material(material),
        )

    def list_courses(self, topic_id=None):
        if topic_id is not None:
            topic = self.topics.require_public(topic_id)
            self.modules.require_public(topic["module_id"])
            return {
                "items": [
                    self.course_summary(course, published_only=True)
                    for course in self._courses_for_topic(topic_id, published_only=True)
                    if self._course_materials_are_public(course)
                ]
            }
        return {"items": self._public_courses()}

    def get_course(
        self,
        course_id,
        include_lesson_content=False,
        unlocked_lesson_count=None,
    ):
        course = self.courses.require_public(course_id)
        if not self._course_topic_rows(course_id, published_only=True):
            raise HTTPException(404, "Learning catalogue record not found.")
        material_rows = self._course_material_rows(course)
        # A course owns an ordered set of whole materials.  A material does not
        # have to live in the course's display topic, but every linked material
        # must itself be published before the course can expose it.
        materials = []
        lessons = []
        lesson_index = 0
        for row in material_rows:
            material = self.materials.require_public(row["id"])
            material_view = self._material_view(material)
            material_view["course_sort_order"] = row["course_material_sort_order"]
            material_view["lessons"] = []
            for lesson in self.material_lessons.dao.list_lessons(material["id"]):
                lesson_view = self._lesson_view(
                    lesson,
                    include_content=include_lesson_content,
                    is_locked=(
                        unlocked_lesson_count is not None
                        and lesson_index >= unlocked_lesson_count
                    ),
                    template=material_view["template"],
                )
                material_view["lessons"].append(lesson_view)
                lessons.append(lesson_view)
                lesson_index += 1
            materials.append(material_view)

        result = self.course_summary(course)
        result["materials"] = materials
        result["material_ids"] = [material["id"] for material in materials]
        result["material_id"] = result["material_ids"][0] if materials else None
        result["lessons"] = lessons
        if len(materials) == 1:
            result["material"] = {
                key: value for key, value in materials[0].items() if key != "lessons"
            }
        return result

    def list_admin_materials(self, q="", topic_id=None, is_published=None, page=1, page_size=20):
        if topic_id is not None:
            self.topics.require_any(topic_id)
        result = self.materials.dao.list_admin_materials(q, topic_id, is_published, page, page_size)
        return {**result, "items": [self._material_view(row) for row in result["items"]]}

    def _topic_statistics(self, topic_id):
        material_condition = m.learning_material.c.topic_id == topic_id
        course_condition = m.learning_topic_course.c.topic_id == topic_id
        lesson_condition = m.learning_material.c.topic_id == topic_id
        return {
            "material_count": self.db.scalar(
                select(func.count()).select_from(m.learning_material).where(material_condition)
            ),
            "published_material_count": self.db.scalar(
                select(func.count()).select_from(m.learning_material).where(
                    material_condition, m.learning_material.c.is_published == 1
                )
            ),
            "lesson_count": self.db.scalar(
                select(func.count())
                .select_from(m.learning_material_lesson.join(m.learning_material))
                .where(lesson_condition)
            ),
            "published_lesson_count": self.db.scalar(
                select(func.count())
                .select_from(m.learning_material_lesson.join(m.learning_material))
                .where(lesson_condition, m.learning_material_lesson.c.is_published == 1)
            ),
            "course_count": self.db.scalar(
                select(func.count()).select_from(m.learning_topic_course).where(course_condition)
            ),
            "published_course_count": self.db.scalar(
                select(func.count())
                .select_from(
                    m.learning_topic_course.join(
                        m.learning_course,
                        m.learning_course.c.id == m.learning_topic_course.c.course_id,
                    )
                )
                .where(course_condition, m.learning_course.c.is_published == 1)
            ),
        }

    def list_admin_topics(self, q="", module_id=None, is_published=None, page=1, page_size=20):
        if module_id is not None:
            self.modules.require_any(module_id)
        result = self.topics.dao.list_admin_topics(q, module_id, is_published, page, page_size)
        return {
            **result,
            "items": [
                {**serialise_catalog(row), "statistics": self._topic_statistics(row["id"])}
                for row in result["items"]
            ],
        }

    def _course_order_display_entries(self, courses):
        """Return course order entries with their linked material labels."""
        return [self.course_summary(course) for course in courses]

    def get_admin_topic(self, topic_id):
        topic = self.topics.require_any(topic_id)
        result = serialise_catalog(topic)
        result["statistics"] = self._topic_statistics(topic_id)
        materials = [
            self._material_view(row)
            for row in self.materials.dao.list_where(
                self.materials.dao.table.c.topic_id == topic_id,
                order_by=self.materials.dao.ordering(),
            )
        ]
        courses = self._courses_for_topic(topic_id)
        result["materials"] = materials
        result["courses"] = self._course_order_display_entries(courses)
        return result

    def get_admin_material(self, material_id):
        result = self._material_view(self.materials.require_any(material_id))
        result["lessons"] = self.material_lessons.list_all(
            self.material_lessons.dao.table.c.material_id == material_id
        )
        result["courses"] = [
            self.course_summary(course) for course in self._courses_for_material(material_id)
        ]
        return result

    def list_admin_material_lessons(self, material_id):
        self.materials.require_any(material_id)
        return {
            "items": self.material_lessons.list_all(
                self.material_lessons.dao.table.c.material_id == material_id
            )
        }

    def list_admin_courses(
        self,
        q="",
        topic_id=None,
        material_id=None,
        access_policy=None,
        is_published=None,
        page=1,
        page_size=20,
    ):
        if topic_id is not None:
            self.topics.require_any(topic_id)
        if material_id is not None:
            self.materials.require_any(material_id)
        result = self.courses.dao.list_admin_courses(
            q,
            topic_id,
            material_id,
            access_policy,
            is_published,
            page,
            page_size,
        )
        return {
            **result,
            "items": [self.course_summary(row) for row in result["items"]],
        }

    def list_templates(self, active_only=False):
        return {"items": self.templates.list_all(active_only=active_only)}

    def save_template(self, payload: s.LearningTemplateInput, actor, template_id=None):
        values = self._template_record_values(payload)
        existing = self.templates.require_any(template_id) if template_id is not None else None
        duplicate = self.db.execute(
            select(m.learning_template.c.id).where(
                m.learning_template.c.template_code == values["template_code"],
                m.learning_template.c.template_version == values["template_version"],
                *(
                    (m.learning_template.c.id != template_id,)
                    if template_id is not None
                    else ()
                ),
            )
        ).first()
        if duplicate:
            raise HTTPException(409, "这个模板编号和版本已经存在。")
        if existing is not None and (
            existing["template_code"] != values["template_code"]
            or existing["template_version"] != values["template_version"]
        ):
            in_use = self.materials.dao.count(
                self.materials.dao.table.c.template_id == template_id
            )
            if in_use:
                raise HTTPException(422, "已有教材正在使用该模板，不能修改模板编号或版本。")
        if existing is None:
            values["created_by"] = actor["id"]
            template_id = self.templates.dao.insert(values)
        else:
            values["updated_by"] = actor["id"]
            self.templates.dao.update(template_id, values)
        self.db.commit()
        return serialise_template(self.templates.require_any(template_id))

    def delete_template(self, template_id):
        self.templates.require_any(template_id)
        if self.materials.dao.count(
            self.materials.dao.table.c.template_id == template_id
        ):
            raise HTTPException(409, "仍有教材使用该模板，不能删除。")
        self.templates.dao.delete(template_id)
        self.db.commit()

    def save_module(self, payload: s.LearningModuleInput, actor, module_id=None):
        values = self._none_when_blank(
            payload.model_dump(),
            ("name_en", "description", "icon", "color", "route_key"),
        )
        row = self.modules.save(module_id, values, actor)
        self.db.commit()
        return serialise_catalog(row)

    def save_topic(self, payload: s.LearningTopicInput, actor, topic_id=None):
        values = self._none_when_blank(payload.model_dump(), ("title_en", "description", "cover_url"))
        self.modules.require_any(values["module_id"])
        row = self.topics.save(topic_id, values, actor)
        self.db.commit()
        return serialise_catalog(row)

    def set_topic_publication(self, topic_id, payload: s.PublicationInput, actor):
        self.topics.require_any(topic_id)
        self.topics.dao.update(topic_id, {
            "is_published": payload.is_published,
            "updated_by": actor["id"],
        })
        self.db.commit()
        return serialise_catalog(self.topics.require_any(topic_id))

    def set_topic_course_order(self, topic_id, payload: s.TopicCourseOrderInput, actor):
        """Persist one complete, stable course sequence for a topic."""
        self.topics.require_any(topic_id)
        mappings = self.topic_courses.dao.list_for_topic(topic_id)
        existing_ids = [mapping["course_id"] for mapping in mappings]
        course_ids = payload.course_ids

        if len(course_ids) != len(set(course_ids)):
            raise HTTPException(422, "course_ids must not contain duplicate courses.")
        if set(course_ids) != set(existing_ids):
            raise HTTPException(
                422,
                "course_ids must contain every course in this topic exactly once.",
            )

        for position, course_id in enumerate(course_ids, start=1):
            mapping = next(
                mapping for mapping in mappings if mapping["course_id"] == course_id
            )
            self.topic_courses.dao.update(
                mapping["id"],
                {"sort_order": position * 10, "updated_by": actor["id"]},
            )
        self.db.commit()
        return {
            "topic_id": topic_id,
            "items": [
                {
                    **self.course_summary(self.courses.require_any(course_id)),
                    "sort_order": position * 10,
                }
                for position, course_id in enumerate(course_ids, start=1)
            ],
        }

    def associate_topic_courses(
        self, topic_id, payload: s.TopicCourseAssociationInput, actor
    ):
        """Associate existing courses with a topic without changing the courses."""
        self.topics.require_any(topic_id)
        course_ids = payload.course_ids
        if len(course_ids) != len(set(course_ids)):
            raise HTTPException(422, "course_ids must not contain duplicate courses.")

        [self.courses.require_any(course_id) for course_id in course_ids]
        current_mappings = self.topic_courses.dao.list_for_topic(topic_id)
        current_course_ids = {mapping["course_id"] for mapping in current_mappings}
        next_sort_order = max(
            (int(mapping["sort_order"] or 0) for mapping in current_mappings),
            default=0,
        )
        for course_id in course_ids:
            if course_id in current_course_ids:
                continue
            next_sort_order += 10
            self.topic_courses.dao.insert(
                {
                    "topic_id": topic_id,
                    "course_id": course_id,
                    "sort_order": next_sort_order,
                    "created_by": actor["id"],
                    "updated_by": actor["id"],
                },
            )
        if course_ids:
            self.db.commit()
        return {
            "topic_id": topic_id,
            "items": [
                self.course_summary(self.courses.require_any(course_id))
                for course_id in course_ids
            ],
        }

    def remove_topic_course(self, topic_id, course_id):
        self.topics.require_any(topic_id)
        self.courses.require_any(course_id)
        mapping = self.db.execute(
            select(m.learning_topic_course.c.id).where(
                m.learning_topic_course.c.topic_id == topic_id,
                m.learning_topic_course.c.course_id == course_id,
            )
        ).first()
        if not mapping:
            raise HTTPException(404, "The course is not associated with this topic.")
        self.topic_courses.dao.delete(mapping[0])
        self.db.commit()

    def save_material(self, payload: s.LearningMaterialInput, actor, material_id=None):
        existing = self.materials.require_any(material_id) if material_id is not None else None
        values = self._none_when_blank(
            payload.model_dump(),
            (
                "title_en",
                "summary",
                "publisher",
                "version_name",
                "cover_url",
                "difficulty_code",
            ),
        )
        self.topics.require_any(values["topic_id"])
        template_was_sent = "template_id" in payload.model_fields_set
        if not template_was_sent and existing is not None:
            values["template_id"] = existing["template_id"]
        elif values["template_id"] is None:
            values["template_id"] = self._default_template_id(values["material_type"])

        if values["template_id"] is not None:
            selected_template = serialise_template(
                self.templates.require_active(values["template_id"])
            )
        else:
            selected_template = self._fallback_template(values["material_type"])

        if existing is not None:
            proposed = {**dict(existing), **values}
            self._validate_template_material_compatibility(proposed, selected_template)
        row = self.materials.save(material_id, values, actor)
        if existing is not None:
            self._sync_inherited_course_titles(existing, values, actor)
        self.db.commit()
        return self._material_view(row)

    def _sync_inherited_course_titles(self, material, values, actor):
        """Keep an inherited course label in step with a renamed material.

        A course can intentionally have its own title.  We only update fields
        that still equal the material's former value, which is how generated
        one-course-per-material entries are initially named.
        """
        title_changed = material["title"] != values["title"]
        old_title_en = material["title_en"] or ""
        new_title_en = values["title_en"] or ""
        title_en_changed = old_title_en != new_title_en
        if not title_changed and not title_en_changed:
            return

        for course in self._courses_for_material(material["id"]):
            updates = {}
            if title_changed and course["title"] == material["title"]:
                updates["title"] = values["title"]
            if title_en_changed and (course["title_en"] or "") == old_title_en:
                updates["title_en"] = values["title_en"]
            if updates:
                updates["updated_by"] = actor["id"]
                self.courses.dao.update(course["id"], updates)

    def _validate_material_lesson_source(self, values):
        if values["lesson_format"] == "courseware":
            if values["source_resource"] or values["source_reference_id"] or values["content_json"]:
                raise HTTPException(
                    422,
                    "A courseware lesson cannot also define legacy source or self-contained content.",
                )
            return
        source_resource = values["source_resource"]
        source_reference_id = values["source_reference_id"]
        content_json = values["content_json"]
        if source_resource is None:
            if source_reference_id is not None:
                raise HTTPException(422, "source_reference_id requires source_resource.")
            if content_json is None:
                raise HTTPException(422, "A lesson needs a source record or self-contained content.")
            return
        if source_reference_id is None:
            raise HTTPException(422, "source_resource requires source_reference_id.")

        if source_resource == "notes":
            note = self.db.execute(
                select(m.english_note.c.id).where(
                    m.english_note.c.id == source_reference_id,
                    m.english_note.c.share_status == 1,
                )
            ).first()
            if not note:
                raise HTTPException(422, "A note material lesson must reference a shared note.")
            return

        # Known platform sources are checked when a lesson is configured, so a
        # spelling error cannot become a broken learner-facing lesson later.
        from app.services.content import ContentService

        try:
            ContentService(self.db).resource_service(source_resource).require(source_reference_id)
        except HTTPException as error:
            raise HTTPException(422, "The material lesson source record is unavailable.") from error

    def save_material_lesson(
        self, material_id, payload: s.LearningMaterialLessonInput, actor, lesson_id=None
    ):
        material = self.materials.require_any(material_id)
        existing = self.material_lessons.require_any(lesson_id) if lesson_id is not None else None
        values = self._none_when_blank(
            payload.model_dump(),
            ("title_en", "summary", "source_resource"),
        )
        content = values.pop("content")
        values["content_json"] = self._encode_json(content, "content")
        values["material_id"] = material["id"]
        if values["is_published"] is None:
            values["is_published"] = (
                existing["is_published"]
                if existing is not None
                else 0 if values["lesson_format"] == "courseware" else 1
            )
        self._validate_material_lesson_source(values)
        if lesson_id is not None:
            if existing["material_id"] != material_id:
                raise HTTPException(409, "The material lesson belongs to a different material.")
        self._validate_lesson_template_compatibility(
            values,
            self._template_for_material(material, require_active=True),
        )
        row = self.material_lessons.save(lesson_id, values, actor)
        self.db.commit()
        return serialise_catalog(row)

    def save_course(self, payload: s.LearningCourseInput, actor, course_id=None):
        values = self._none_when_blank(
            payload.model_dump(),
            ("title_en", "summary", "content_resource", "cover_url", "difficulty_code"),
        )
        content = values.pop("content")
        values["content_json"] = self._encode_json(content, "content")
        legacy_topic_id = values.pop("topic_id", None)
        if legacy_topic_id is not None:
            self.topics.require_any(legacy_topic_id)
        material_ids = list(values.pop("material_ids", []))
        legacy_material_id = values.pop("material_id", None)
        # Older integrations only submit material_id.  For new clients the
        # ordered material_ids list is authoritative, including an empty list.
        if not material_ids and legacy_material_id is not None:
            material_ids = [legacy_material_id]
        if len(material_ids) != len(set(material_ids)):
            raise HTTPException(422, "material_ids must not contain duplicate materials.")
        for material_id in material_ids:
            self.materials.require_any(material_id)
        if material_ids and (
            values["content_resource"]
            or values["content_reference_id"]
            or values["content_json"]
        ):
            raise HTTPException(
                422,
                "A course linked to materials cannot also define legacy direct content.",
            )

        # Retain the first material in the old column while existing callers
        # migrate; all reads and writes use learning_course_material instead.
        values["material_id"] = material_ids[0] if material_ids else None
        row = self.courses.save(course_id, values, actor)
        self._replace_course_materials(row["id"], material_ids, actor)
        if legacy_topic_id is not None:
            mapped_course_ids = {
                mapping["course_id"]
                for mapping in self.topic_courses.dao.list_for_topic(legacy_topic_id)
            }
            if row["id"] not in mapped_course_ids:
                next_sort_order = max(
                    (
                        int(mapping["sort_order"] or 0)
                        for mapping in self.topic_courses.dao.list_for_topic(legacy_topic_id)
                    ),
                    default=0,
                )
                self.topic_courses.dao.insert(
                    {
                        "topic_id": legacy_topic_id,
                        "course_id": row["id"],
                        "sort_order": next_sort_order + 10,
                        "created_by": actor["id"],
                        "updated_by": actor["id"],
                    }
                )
        self.db.commit()
        return self.course_summary(self.courses.require_any(row["id"]))

    def delete_module(self, module_id):
        self.modules.require_any(module_id)
        if self.topics.dao.count(self.topics.dao.table.c.module_id == module_id):
            raise HTTPException(409, "Delete this module's topics before deleting the module.")
        self.modules.delete(module_id)
        self.db.commit()

    def delete_topic(self, topic_id):
        self.topics.require_any(topic_id)
        if self.topic_courses.dao.count(
            self.topic_courses.dao.table.c.topic_id == topic_id
        ):
            raise HTTPException(409, "Delete this topic's courses before deleting the topic.")
        if self.materials.dao.count(self.materials.dao.table.c.topic_id == topic_id):
            raise HTTPException(409, "Delete this topic's materials before deleting the topic.")
        self.topics.delete(topic_id)
        self.db.commit()

    def delete_material(self, material_id):
        self.materials.require_any(material_id)
        if self.material_lessons.dao.count(self.material_lessons.dao.table.c.material_id == material_id):
            raise HTTPException(409, "Delete this material's lessons before deleting the material.")
        if self._courses_for_material(material_id):
            raise HTTPException(409, "Detach this material from its courses before deleting it.")
        self.materials.delete(material_id)
        self.db.commit()

    def delete_material_lesson(self, lesson_id):
        self.material_lessons.delete(lesson_id)
        self.db.commit()

    def delete_course(self, course_id):
        self.courses.require_any(course_id)
        references = (
            ("会员权益", m.membership_benefit_course),
            ("用户课程", m.learning_user_course),
            ("学习进度", m.learning_progress),
            ("学习会话", m.learning_study_session),
        )
        in_use_by = [
            label
            for label, table in references
            if self.db.scalar(
                select(func.count())
                .select_from(table)
                .where(table.c.course_id == course_id)
            )
        ]
        if in_use_by:
            raise HTTPException(
                409,
                f"课程仍被{'、'.join(in_use_by)}引用，不能移除。",
            )
        # Delete the mappings explicitly as well as relying on the database
        # cascade. This also works in development SQLite databases where
        # foreign-key enforcement may not be enabled.
        self.course_materials.dao.delete_where(
            self.course_materials.dao.table.c.course_id == course_id
        )
        self.topic_courses.dao.delete_where(
            self.topic_courses.dao.table.c.course_id == course_id
        )
        self.courses.delete(course_id)
        self.db.commit()
