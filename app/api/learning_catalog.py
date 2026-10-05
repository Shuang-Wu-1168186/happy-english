"""HTTP controllers for the learning module → topic → course catalogue."""

from fastapi import APIRouter, Query

from app.api.dependencies import Admin, Db, User
from app.schemas import (
    CoursewareBlockInput,
    CoursewareBlockSourcesInput,
    LearningCourseInput,
    LearningMaterialInput,
    LearningMaterialLessonInput,
    LearningModuleInput,
    LearningLessonSectionsInput,
    LearningTemplateInput,
    LearningTopicInput,
    NoteCoursewareGenerateInput,
    NoteCoursewarePreviewInput,
    PublicationInput,
    TopicCourseAssociationInput,
    TopicCourseOrderInput,
)
from app.services.courseware import CoursewareBlockService, NoteCoursewareService
from app.services.learning_catalog import LearningCatalogService

router = APIRouter(tags=["learning-catalog"])


ADMIN_MANAGEMENT_MENU = [
    {
        "code": "learning-content",
        "title": "学习内容管理",
        "icon": "book-open",
        "children": [
            {
                "code": "topic-maintenance",
                "title": "专题维护",
                "path": "/admin/content/topics",
                "description": "维护专题、专题内课程管理、封面和发布状态。",
            },
            {
                "code": "material-maintenance",
                "title": "教材开发",
                "path": "/admin/learning/materials",
                "description": "开发教材并编排教材内的多个课时。",
            },
            {
                "code": "template-maintenance",
                "title": "模板管理",
                "path": "/admin/content/templates",
                "description": "维护 Web 和小程序共用的教材渲染模板。",
            },
            {
                "code": "course-maintenance",
                "title": "课程开发",
                "path": "/admin/learning/courses",
                "description": "组合多个教材，并设置免费或会员权益课程。",
            },
        ],
    }
]


@router.get("/admin/management-menu")
def get_admin_management_menu(admin: Admin):
    return {"items": ADMIN_MANAGEMENT_MENU}


@router.get("/admin/courseware/source-notes")
def list_courseware_source_notes(db: Db, admin: Admin):
    return NoteCoursewareService(db).list_notes()


@router.get("/admin/courseware/source-notes/{note_id}/items")
def list_courseware_source_note_items(note_id: int, db: Db, admin: Admin):
    return NoteCoursewareService(db).list_note_items(note_id)


@router.post("/admin/courseware/note-preview")
def preview_note_courseware(payload: NoteCoursewarePreviewInput, db: Db, admin: Admin):
    return NoteCoursewareService(db).preview(payload.note_item_id)


@router.post("/admin/courseware/from-note-item", status_code=201)
def generate_note_courseware(payload: NoteCoursewareGenerateInput, db: Db, admin: Admin):
    return NoteCoursewareService(db).generate(
        payload.note_item_id, payload.topic_id, admin, payload.material_id
    )


@router.get("/learning/modules")
def list_modules(db: Db, user: User):
    return LearningCatalogService(db).list_modules()


@router.get("/learning/modules/{module_id}")
def get_module(module_id: int, db: Db, user: User):
    return LearningCatalogService(db).get_module(module_id)


@router.get("/learning/topics")
def list_topics(db: Db, user: User, module_id: int | None = Query(default=None, gt=0)):
    return LearningCatalogService(db).list_topics(module_id)


@router.get("/learning/topics/{topic_id}")
def get_topic(topic_id: int, db: Db, user: User):
    return LearningCatalogService(db).get_topic(topic_id)


@router.get("/learning/materials")
def list_materials(db: Db, user: User, topic_id: int | None = Query(default=None, gt=0)):
    return LearningCatalogService(db).list_materials(topic_id)


@router.get("/learning/templates")
def list_learning_templates(db: Db, user: User):
    return LearningCatalogService(db).list_templates(active_only=True)


@router.get("/learning/materials/{material_id}")
def get_material(material_id: int, db: Db, user: User):
    return LearningCatalogService(db).get_material(material_id, user=user)


@router.get("/learning/materials/{material_id}/lessons/{lesson_id}")
def get_material_lesson(material_id: int, lesson_id: int, db: Db, user: User):
    return LearningCatalogService(db).get_material_lesson(material_id, lesson_id, user=user)


@router.get("/learning/courses")
def list_courses(db: Db, user: User, topic_id: int | None = Query(default=None, gt=0)):
    return LearningCatalogService(db).list_courses(topic_id)


@router.get("/learning/courses/{course_id}")
def get_course(course_id: int, db: Db, user: User):
    return LearningCatalogService(db).get_course(course_id)


@router.post("/admin/learning/modules", status_code=201)
def create_module(payload: LearningModuleInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_module(payload, admin)


@router.put("/admin/learning/modules/{module_id}")
def update_module(module_id: int, payload: LearningModuleInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_module(payload, admin, module_id)


@router.delete("/admin/learning/modules/{module_id}", status_code=204)
def delete_module(module_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_module(module_id)


@router.post("/admin/learning/topics", status_code=201)
def create_topic(payload: LearningTopicInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_topic(payload, admin)


@router.put("/admin/learning/topics/{topic_id}")
def update_topic(topic_id: int, payload: LearningTopicInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_topic(payload, admin, topic_id)


@router.put("/admin/learning/topics/{topic_id}/publication")
def set_topic_publication(topic_id: int, payload: PublicationInput, db: Db, admin: Admin):
    return LearningCatalogService(db).set_topic_publication(topic_id, payload, admin)


@router.put("/admin/learning-topics/{topic_id}/course-order")
def set_topic_course_order(
    topic_id: int,
    payload: TopicCourseOrderInput,
    db: Db,
    admin: Admin,
):
    return LearningCatalogService(db).set_topic_course_order(topic_id, payload, admin)


@router.post("/admin/learning-topics/{topic_id}/courses")
def associate_topic_courses(
    topic_id: int,
    payload: TopicCourseAssociationInput,
    db: Db,
    admin: Admin,
):
    return LearningCatalogService(db).associate_topic_courses(topic_id, payload, admin)


@router.delete("/admin/learning-topics/{topic_id}/courses/{course_id}", status_code=204)
def remove_topic_course(topic_id: int, course_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).remove_topic_course(topic_id, course_id)


@router.delete("/admin/learning/topics/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_topic(topic_id)


@router.get("/admin/learning-topics")
def list_admin_topics(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    module_id: int | None = Query(default=None, gt=0),
    is_published: int | None = Query(default=None, ge=0, le=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return LearningCatalogService(db).list_admin_topics(
        q, module_id, is_published, page, page_size
    )


@router.get("/admin/learning-topics/{topic_id}")
def get_admin_topic(topic_id: int, db: Db, admin: Admin):
    return LearningCatalogService(db).get_admin_topic(topic_id)


@router.get("/admin/learning-materials")
def list_admin_materials(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    topic_id: int | None = Query(default=None, gt=0),
    is_published: int | None = Query(default=None, ge=0, le=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return LearningCatalogService(db).list_admin_materials(
        q, topic_id, is_published, page, page_size
    )


@router.get("/admin/learning-templates")
def list_admin_learning_templates(db: Db, admin: Admin):
    return LearningCatalogService(db).list_templates()


@router.post("/admin/learning-templates", status_code=201)
def create_learning_template(payload: LearningTemplateInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_template(payload, admin)


@router.put("/admin/learning-templates/{template_id}")
def update_learning_template(
    template_id: int, payload: LearningTemplateInput, db: Db, admin: Admin
):
    return LearningCatalogService(db).save_template(payload, admin, template_id)


@router.delete("/admin/learning-templates/{template_id}", status_code=204)
def delete_learning_template(template_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_template(template_id)


@router.post("/admin/learning-materials", status_code=201)
def create_material(payload: LearningMaterialInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_material(payload, admin)


@router.get("/admin/learning-materials/{material_id}")
def get_admin_material(material_id: int, db: Db, admin: Admin):
    return LearningCatalogService(db).get_admin_material(material_id)


@router.put("/admin/learning-materials/{material_id}")
def update_material(material_id: int, payload: LearningMaterialInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_material(payload, admin, material_id)


@router.delete("/admin/learning-materials/{material_id}", status_code=204)
def delete_material(material_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_material(material_id)


@router.get("/admin/learning-materials/{material_id}/lessons")
def list_admin_material_lessons(material_id: int, db: Db, admin: Admin):
    return LearningCatalogService(db).list_admin_material_lessons(material_id)


@router.post("/admin/learning-materials/{material_id}/lessons", status_code=201)
def create_material_lesson(
    material_id: int,
    payload: LearningMaterialLessonInput,
    db: Db,
    admin: Admin,
):
    return LearningCatalogService(db).save_material_lesson(material_id, payload, admin)


@router.put("/admin/learning-material-lessons/{lesson_id}")
def update_material_lesson(lesson_id: int, payload: LearningMaterialLessonInput, db: Db, admin: Admin):
    service = LearningCatalogService(db)
    lesson = service.material_lessons.require_any(lesson_id)
    return service.save_material_lesson(lesson["material_id"], payload, admin, lesson_id)


@router.delete("/admin/learning-material-lessons/{lesson_id}", status_code=204)
def delete_material_lesson(lesson_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_material_lesson(lesson_id)


@router.get("/admin/learning-material-lessons/{lesson_id}/sections")
def list_learning_lesson_sections(lesson_id: int, db: Db, admin: Admin):
    return {
        "items": LearningCatalogService(db).lesson_content.list_for_lesson(
            lesson_id, published_only=False
        )
    }


@router.put("/admin/learning-material-lessons/{lesson_id}/sections")
def replace_learning_lesson_sections(
    lesson_id: int,
    payload: LearningLessonSectionsInput,
    db: Db,
    admin: Admin,
):
    service = LearningCatalogService(db)
    return service.lesson_content.replace(lesson_id, payload, admin)


@router.post("/admin/learning-material-lessons/{lesson_id}/publish")
def publish_learning_lesson(lesson_id: int, db: Db, admin: Admin):
    return LearningCatalogService(db).lesson_content.publish(lesson_id, admin)


@router.get("/admin/learning-material-lessons/{lesson_id}/courseware-blocks")
def list_courseware_blocks(lesson_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).material_lessons.require_any(lesson_id)
    service = CoursewareBlockService(db)
    return {"items": service.list_for_lesson(lesson_id, include_sources=True)}


@router.post("/admin/learning-material-lessons/{lesson_id}/courseware-blocks", status_code=201)
def create_courseware_block(
    lesson_id: int,
    payload: CoursewareBlockInput,
    db: Db,
    admin: Admin,
):
    return CoursewareBlockService(db).save(lesson_id, payload, admin)


@router.put("/admin/courseware-blocks/{block_id}")
def update_courseware_block(
    block_id: int,
    payload: CoursewareBlockInput,
    db: Db,
    admin: Admin,
):
    service = CoursewareBlockService(db)
    block = service.require_any(block_id)
    return service.save(block["material_lesson_id"], payload, admin, block_id)


@router.put("/admin/courseware-blocks/{block_id}/sources")
def replace_courseware_block_sources(
    block_id: int,
    payload: CoursewareBlockSourcesInput,
    db: Db,
    admin: Admin,
):
    return {"items": CoursewareBlockService(db).replace_sources(block_id, payload)}


@router.delete("/admin/courseware-blocks/{block_id}", status_code=204)
def delete_courseware_block(block_id: int, db: Db, admin: Admin):
    CoursewareBlockService(db).delete(block_id)


@router.get("/admin/learning-courses")
def list_admin_courses(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    topic_id: int | None = Query(default=None, gt=0),
    material_id: int | None = Query(default=None, gt=0),
    access_policy: str | None = Query(default=None, pattern="^(free|benefit)$"),
    is_published: int | None = Query(default=None, ge=0, le=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return LearningCatalogService(db).list_admin_courses(
        q,
        topic_id,
        material_id,
        access_policy,
        is_published,
        page,
        page_size,
    )


@router.post("/admin/learning/courses", status_code=201)
def create_course(payload: LearningCourseInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_course(payload, admin)


@router.put("/admin/learning/courses/{course_id}")
def update_course(course_id: int, payload: LearningCourseInput, db: Db, admin: Admin):
    return LearningCatalogService(db).save_course(payload, admin, course_id)


@router.delete("/admin/learning/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Db, admin: Admin):
    LearningCatalogService(db).delete_course(course_id)
