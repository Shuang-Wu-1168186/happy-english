"""DAOs for learning modules, topics, materials, material lessons, and courses."""

from sqlalchemy import or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class LearningCatalogTableDAO(BaseTableDAO):
    """Shared ordered, published-only reads for catalogue records."""

    def visible_conditions(self):
        return [self.table.c.is_published == 1]

    def ordering(self):
        return [self.table.c.sort_order, self.table.c.id]

    def get_published(self, item_id):
        return self.find_by_id(item_id, *self.visible_conditions())

    def list_published(self, *conditions):
        return self.list_where(*conditions, *self.visible_conditions(), order_by=self.ordering())


class LearningModuleDAO(LearningCatalogTableDAO):
    table = m.learning_module

    def list_modules(self):
        return self.list_published()


class LearningTopicDAO(LearningCatalogTableDAO):
    table = m.learning_topic

    def list_topics(self, module_id=None):
        conditions = []
        if module_id is not None:
            conditions.append(self.table.c.module_id == module_id)
        return self.list_published(*conditions)

    def list_admin_topics(self, q="", module_id=None, is_published=None, page=1, page_size=20):
        conditions = []
        if q:
            conditions.append(
                or_(
                    self.table.c.topic_code.ilike(f"%{q}%"),
                    self.table.c.title.ilike(f"%{q}%"),
                    self.table.c.title_en.ilike(f"%{q}%"),
                    self.table.c.description.ilike(f"%{q}%"),
                )
            )
        if module_id is not None:
            conditions.append(self.table.c.module_id == module_id)
        if is_published is not None:
            conditions.append(self.table.c.is_published == is_published)
        return self.paginate_where(
            *conditions,
            order_by=self.ordering(),
            page=page,
            page_size=page_size,
        )


class LearningTemplateDAO(BaseTableDAO):
    """Persist the stable renderer contract shared by every client."""

    table = m.learning_template

    def ordering(self):
        return [self.table.c.sort_order, self.table.c.id]

    def list_active(self):
        return self.list_where(
            self.table.c.status == "active", order_by=self.ordering()
        )


class LearningMaterialDAO(LearningCatalogTableDAO):
    table = m.learning_material

    def list_materials(self, topic_id=None):
        conditions = []
        if topic_id is not None:
            conditions.append(self.table.c.topic_id == topic_id)
        return self.list_published(*conditions)

    def list_admin_materials(self, q="", topic_id=None, is_published=None, page=1, page_size=20):
        conditions = []
        if q:
            conditions.append(
                or_(
                    self.table.c.material_code.ilike(f"%{q}%"),
                    self.table.c.title.ilike(f"%{q}%"),
                    self.table.c.title_en.ilike(f"%{q}%"),
                    self.table.c.publisher.ilike(f"%{q}%"),
                    self.table.c.version_name.ilike(f"%{q}%"),
                )
            )
        if topic_id is not None:
            conditions.append(self.table.c.topic_id == topic_id)
        if is_published is not None:
            conditions.append(self.table.c.is_published == is_published)
        return self.paginate_where(
            *conditions,
            order_by=self.ordering(),
            page=page,
            page_size=page_size,
        )


class LearningMaterialLessonDAO(LearningCatalogTableDAO):
    table = m.learning_material_lesson

    def list_lessons(self, material_id=None):
        conditions = []
        if material_id is not None:
            conditions.append(self.table.c.material_id == material_id)
        return self.list_published(*conditions)


class LearningCourseDAO(LearningCatalogTableDAO):
    table = m.learning_course

    def list_courses(self):
        return self.list_published()

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
        conditions = []
        if q:
            conditions.append(
                or_(
                    self.table.c.course_code.ilike(f"%{q}%"),
                    self.table.c.title.ilike(f"%{q}%"),
                    self.table.c.title_en.ilike(f"%{q}%"),
                    self.table.c.course_type.ilike(f"%{q}%"),
                )
            )
        if topic_id is not None:
            topic_course_ids = select(m.learning_topic_course.c.course_id).where(
                m.learning_topic_course.c.topic_id == topic_id
            )
            conditions.append(self.table.c.id.in_(topic_course_ids))
        if material_id is not None:
            mapped_course_ids = select(m.learning_course_material.c.course_id).where(
                m.learning_course_material.c.material_id == material_id
            )
            # The legacy field is included until every deployed database has
            # executed the backfill migration.
            conditions.append(
                or_(
                    self.table.c.id.in_(mapped_course_ids),
                    self.table.c.material_id == material_id,
                )
            )
        if access_policy:
            conditions.append(self.table.c.access_policy == access_policy)
        if is_published is not None:
            conditions.append(self.table.c.is_published == is_published)
        return self.paginate_where(
            *conditions,
            order_by=self.ordering(),
            page=page,
            page_size=page_size,
        )


class LearningCourseMaterialDAO(BaseTableDAO):
    """Persist the ordered course-to-material mapping."""

    table = m.learning_course_material

    def ordering(self):
        return [self.table.c.sort_order, self.table.c.id]

    def list_for_course(self, course_id):
        return self.list_where(
            self.table.c.course_id == course_id,
            order_by=self.ordering(),
        )


class LearningTopicCourseDAO(BaseTableDAO):
    """Persist the ordered many-to-many topic-to-course mapping."""

    table = m.learning_topic_course

    def ordering(self):
        return [self.table.c.sort_order, self.table.c.id]

    def list_for_topic(self, topic_id):
        return self.list_where(
            self.table.c.topic_id == topic_id,
            order_by=self.ordering(),
        )

    def list_for_course(self, course_id):
        return self.list_where(
            self.table.c.course_id == course_id,
            order_by=self.ordering(),
        )


LEARNING_CATALOG_TABLE_DAO_TYPES = {
    m.learning_module.name: LearningModuleDAO,
    m.learning_topic.name: LearningTopicDAO,
    m.learning_template.name: LearningTemplateDAO,
    m.learning_material.name: LearningMaterialDAO,
    m.learning_material_lesson.name: LearningMaterialLessonDAO,
    m.learning_course.name: LearningCourseDAO,
    m.learning_topic_course.name: LearningTopicCourseDAO,
    m.learning_course_material.name: LearningCourseMaterialDAO,
}
