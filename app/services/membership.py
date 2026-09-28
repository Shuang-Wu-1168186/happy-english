"""Membership configuration, course entitlement, and my-course services."""

import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select

from app import models as m
from app import schemas as s
from app.dao.accounts import UserDAO
from app.dao.membership import (
    LearningUserCourseDAO,
    MembershipBenefitCourseDAO,
    MembershipBenefitDAO,
    MembershipPlanBenefitDAO,
    MembershipPlanDAO,
    UserMembershipDAO,
)
from app.services.learning_catalog import LearningCatalogService, LearningCourseService


# A membership course still gives learners a useful, concrete trial.  The
# count is intentionally applied to material lessons (the navigable course
# units), rather than raw sentences, cards, or dialogue lines.
FREE_PREVIEW_LESSON_COUNT = 2


def serialise_membership(row):
    """Decode persisted JSON values into the API fields used by the admin UI."""
    result = dict(row)
    for key, value in list(result.items()):
        if not key.endswith("_json"):
            continue
        result.pop(key)
        output_key = key.removesuffix("_json")
        if value is None:
            result[output_key] = None
            continue
        try:
            result[output_key] = json.loads(value)
        except (TypeError, ValueError):
            result[output_key] = None
    return result


class MembershipTableService:
    """Common CRUD helpers for the membership configuration tables."""

    dao_type = None

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def require(self, item_id):
        row = self.dao.find_by_id(item_id)
        if not row:
            raise HTTPException(404, "Membership record not found.")
        return row


class MembershipPlanService(MembershipTableService):
    dao_type = MembershipPlanDAO

    def list(self, q="", status=None, page=1, page_size=20):
        result = self.dao.list_plans(q, status, page, page_size)
        return {**result, "items": [serialise_membership(row) for row in result["items"]]}


class MembershipBenefitService(MembershipTableService):
    dao_type = MembershipBenefitDAO

    def list(self, q="", status=None, benefit_type=None, page=1, page_size=20):
        result = self.dao.list_benefits(q, status, benefit_type, page, page_size)
        return {**result, "items": [serialise_membership(row) for row in result["items"]]}


class MembershipPlanBenefitService(MembershipTableService):
    dao_type = MembershipPlanBenefitDAO

    def list_for_plan(self, plan_id):
        return [serialise_membership(row) for row in self.dao.list_for_plan(plan_id)]


class UserMembershipService(MembershipTableService):
    dao_type = UserMembershipDAO

    def list_for_user(self, user_id):
        return [serialise_membership(row) for row in self.dao.list_for_user(user_id)]


class MembershipBenefitCourseService(MembershipTableService):
    dao_type = MembershipBenefitCourseDAO

    def list_for_benefit(self, benefit_id):
        catalog = LearningCatalogService(self.db)
        items = []
        for row in self.dao.list_for_benefit(benefit_id):
            course = catalog.course_summary(catalog.courses.require_any(row["course_id"]))
            items.append(
                {
                    **serialise_membership(row),
                    "material_ids": course["material_ids"],
                    "materials": course["materials"],
                    "material_titles": course.get("material_titles", ""),
                    "material_title": course.get("material_title"),
                }
            )
        return items


class LearningUserCourseService(MembershipTableService):
    dao_type = LearningUserCourseDAO

    def __init__(self, db):
        super().__init__(db)
        self.courses = LearningCourseService(db)
        self.catalog = LearningCatalogService(db)
        self.user_memberships = UserMembershipService(db)
        self.plan_benefits = MembershipPlanBenefitService(db)
        self.benefit_courses = MembershipBenefitCourseService(db)

    def course_access(self, user_id, course):
        """Resolve current access without persisting a duplicate entitlement flag."""
        if course["is_published"] != 1:
            return {"access_state": "unavailable", "membership_id": None}
        if course["access_policy"] == "free":
            return {"access_state": "available", "membership_id": None}

        benefit_ids = self.benefit_courses.dao.enabled_benefit_ids_for_course(course["id"])
        if not benefit_ids:
            return {"access_state": "locked", "membership_id": None}
        memberships = self.user_memberships.dao.active_for_user(user_id)
        granted_ids = set(
            self.plan_benefits.dao.enabled_benefit_ids_for_plans(
                [row["membership_plan_id"] for row in memberships],
                benefit_ids,
            )
        )
        if not granted_ids:
            return {"access_state": "locked", "membership_id": None}
        membership = next(
            (
                row
                for row in memberships
                if set(
                    self.plan_benefits.dao.enabled_benefit_ids_for_plans(
                        [row["membership_plan_id"]], benefit_ids
                    )
                )
                & granted_ids
            ),
            None,
        )
        return {
            "access_state": "available",
            "membership_id": membership["id"] if membership else None,
        }

    def material_access(self, user_id, material_id):
        """Resolve lesson access when a learner enters through a material.

        The public catalogue now opens a material directly, while membership
        is still configured on courses.  A material may belong to several
        courses, so it is available in full when any linked course is free or
        already entitled.  Otherwise only the first two lessons in the linked
        course sequence are previewable.
        """
        linked_courses = []
        unlocked_indexes = set()
        has_membership_course = False
        catalog = self.catalog

        for course in catalog._courses_for_material(material_id):
            if course["is_published"] != 1:
                continue
            material_rows = catalog._course_material_rows(course, published_only=True)
            material_position = next(
                (
                    position
                    for position, row in enumerate(material_rows)
                    if row["id"] == material_id
                ),
                None,
            )
            if material_position is None:
                continue
            linked_courses.append(course)
            access = self.course_access(user_id, course)
            if course["access_policy"] == "benefit":
                has_membership_course = True
            if access["access_state"] == "available":
                return {
                    "access_state": "available",
                    "membership_id": access.get("membership_id"),
                    "preview_lesson_count": None,
                    "requires_membership": course["access_policy"] == "benefit",
                    "unlocked_lesson_indexes": None,
                }

            # Preview count is global to a course, including lessons in
            # materials that come before this one.
            preceding_lessons = sum(
                len(catalog.material_lessons.dao.list_lessons(row["id"]))
                for row in material_rows[:material_position]
            )
            material_lesson_count = len(
                catalog.material_lessons.dao.list_lessons(material_id)
            )
            remaining_preview = max(0, FREE_PREVIEW_LESSON_COUNT - preceding_lessons)
            unlocked_indexes.update(range(min(material_lesson_count, remaining_preview)))

        if not linked_courses:
            return {
                "access_state": "available",
                "membership_id": None,
                "preview_lesson_count": None,
                "requires_membership": False,
                "unlocked_lesson_indexes": None,
            }
        return {
            "access_state": "preview",
            "membership_id": None,
            "preview_lesson_count": FREE_PREVIEW_LESSON_COUNT,
            "requires_membership": has_membership_course,
            "unlocked_lesson_indexes": sorted(unlocked_indexes),
        }

    def enroll(self, user, course_id):
        course = self.courses.require_public(course_id)
        access = self.course_access(user["id"], course)
        if access["access_state"] != "available":
            raise HTTPException(403, "This course requires an active membership benefit.")
        existing = self.dao.find_for_user_course(user["id"], course_id)
        if existing:
            self.dao.update(
                existing["id"],
                {
                    "status": "active",
                    "archived_at": None,
                    "last_opened_at": func.now(),
                },
            )
            row = self.dao.find_by_id(existing["id"])
        else:
            enrollment_id = self.dao.insert(
                {
                    "user_id": user["id"],
                    "course_id": course_id,
                    "source": "membership" if access["membership_id"] else "self_added",
                    "source_membership_id": access["membership_id"],
                    "status": "active",
                    "last_opened_at": func.now(),
                }
            )
            row = self.dao.find_by_id(enrollment_id)
        self.db.commit()
        return {**serialise_membership(row), **access}

    def list_for_user(self, user_id):
        items = []
        for row in self.dao.list_for_user(user_id):
            course = {
                "id": row["course_id"],
                "is_published": row["course_is_published"],
                "access_policy": row["access_policy"],
            }
            summary = self.catalog.course_summary(
                self.catalog.courses.require_any(row["course_id"])
            )
            items.append(
                {
                    **serialise_membership(row),
                    "material_ids": summary["material_ids"],
                    "materials": summary["materials"],
                    "material_titles": summary.get("material_titles", ""),
                    "material_title": summary.get("material_title"),
                    **self.course_access(user_id, course),
                }
            )
        return {"items": items}

    def archive(self, user_id, course_id):
        row = self.dao.find_for_user_course(user_id, course_id)
        if not row:
            raise HTTPException(404, "Course is not in this user's course list.")
        self.dao.update(row["id"], {"status": "archived", "archived_at": func.now()})
        self.db.commit()


MEMBERSHIP_TABLE_SERVICE_TYPES = {
    "membership_plan": MembershipPlanService,
    "membership_benefit": MembershipBenefitService,
    "membership_plan_benefit": MembershipPlanBenefitService,
    "user_membership": UserMembershipService,
    "membership_benefit_course": MembershipBenefitCourseService,
    "learning_user_course": LearningUserCourseService,
}


class MembershipService:
    """Use cases spanning membership configuration and course entitlement."""

    def __init__(self, db):
        self.db = db
        self.users = UserDAO(db)
        self.plans = MembershipPlanService(db)
        self.benefits = MembershipBenefitService(db)
        self.plan_benefits = MembershipPlanBenefitService(db)
        self.user_memberships = UserMembershipService(db)
        self.benefit_courses = MembershipBenefitCourseService(db)
        self.user_courses = LearningUserCourseService(db)
        self.courses = LearningCourseService(db)

    def uses_membership_course_entry(self, resource):
        """Whether a resource is published only through a benefit course.

        The legacy content API has no course context, so it cannot apply a
        per-lesson preview safely. Member content must enter through the
        course-opening API, which supplies the two lesson preview and omits
        locked lesson bodies.
        """
        course = m.learning_course
        course_material = m.learning_course_material
        lesson = m.learning_material_lesson
        return bool(
            self.db.scalar(
                select(course.c.id)
                .outerjoin(course_material, course_material.c.course_id == course.c.id)
                .outerjoin(
                    lesson,
                    or_(
                        lesson.c.material_id == course_material.c.material_id,
                        and_(
                            course_material.c.id.is_(None),
                            lesson.c.material_id == course.c.material_id,
                        ),
                    ),
                )
                .where(
                    course.c.is_published == 1,
                    course.c.access_policy == "benefit",
                    or_(
                        and_(
                            lesson.c.is_published == 1,
                            lesson.c.source_resource == resource,
                        ),
                        course.c.content_resource == resource,
                    ),
                )
                .limit(1)
            )
        )

    def can_open_legacy_content(self, user, resource):
        return user["role"] == "admin" or not self.uses_membership_course_entry(resource)

    def require_legacy_content_access(self, user, resource):
        if not self.can_open_legacy_content(user, resource):
            raise HTTPException(403, "请从课程页面进入会员学习内容。")

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
    def _validate_value(value, value_type, field_name):
        if value is None:
            return
        valid = {
            "boolean": isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "decimal": isinstance(value, (int, float, Decimal)) and not isinstance(value, bool),
            "string": isinstance(value, str),
            "json": True,
        }
        if not valid[value_type]:
            raise HTTPException(422, f"{field_name} does not match the benefit value_type.")

    @staticmethod
    def _naive_utc(value):
        if value is None or value.tzinfo is None:
            return value
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def list_plans(self, q="", status=None, page=1, page_size=20):
        return self.plans.list(q, status, page, page_size)

    def get_plan(self, plan_id):
        result = serialise_membership(self.plans.require(plan_id))
        result["benefits"] = self.plan_benefits.list_for_plan(plan_id)
        return result

    def save_plan(self, payload: s.MembershipPlanInput, actor, plan_id=None):
        values = self._none_when_blank(
            payload.model_dump(),
            ("name_en", "description", "icon", "badge_text"),
        )
        if values["billing_cycle"] == "lifetime" and values["duration_days"] is not None:
            raise HTTPException(422, "A lifetime membership cannot have duration_days.")
        if values["is_default"] and values["status"] != "active":
            raise HTTPException(422, "The default membership plan must be active.")
        if plan_id is not None:
            existing = self.plans.require(plan_id)
            if existing["plan_code"] != values["plan_code"]:
                raise HTTPException(422, "plan_code cannot be changed after creation.")
        if values["is_default"]:
            self.plans.dao.clear_default(plan_id)
        if plan_id is None:
            values["created_by"] = actor["id"]
            plan_id = self.plans.dao.insert(values)
        else:
            values["updated_by"] = actor["id"]
            self.plans.dao.update(plan_id, values)
        self.db.commit()
        return serialise_membership(self.plans.require(plan_id))

    def delete_plan(self, plan_id):
        self.plans.require(plan_id)
        if self.user_memberships.dao.count(self.user_memberships.dao.table.c.membership_plan_id == plan_id):
            raise HTTPException(409, "A plan with issued memberships cannot be deleted.")
        if self.plan_benefits.dao.count(self.plan_benefits.dao.table.c.membership_plan_id == plan_id):
            raise HTTPException(409, "Remove the plan's benefit mappings before deleting it.")
        self.plans.dao.delete(plan_id)
        self.db.commit()

    def list_benefits(self, q="", status=None, benefit_type=None, page=1, page_size=20):
        return self.benefits.list(q, status, benefit_type, page, page_size)

    def get_benefit(self, benefit_id):
        result = serialise_membership(self.benefits.require(benefit_id))
        result["courses"] = self.benefit_courses.list_for_benefit(benefit_id)
        return result

    def save_benefit(self, payload: s.MembershipBenefitInput, actor, benefit_id=None):
        values = self._none_when_blank(
            payload.model_dump(),
            ("name_en", "description", "unit", "icon"),
        )
        self._validate_value(values["default_value"], values["value_type"], "default_value")
        values["scope_json"] = self._encode_json(values.pop("scope"), "scope")
        values["default_value_json"] = self._encode_json(values.pop("default_value"), "default_value")
        if benefit_id is not None:
            existing = self.benefits.require(benefit_id)
            if existing["benefit_code"] != values["benefit_code"]:
                raise HTTPException(422, "benefit_code cannot be changed after creation.")
        if benefit_id is None:
            values["created_by"] = actor["id"]
            benefit_id = self.benefits.dao.insert(values)
        else:
            values["updated_by"] = actor["id"]
            self.benefits.dao.update(benefit_id, values)
        self.db.commit()
        return serialise_membership(self.benefits.require(benefit_id))

    def delete_benefit(self, benefit_id):
        self.benefits.require(benefit_id)
        if self.plan_benefits.dao.count(self.plan_benefits.dao.table.c.benefit_id == benefit_id):
            raise HTTPException(409, "Remove this benefit from membership plans before deleting it.")
        if self.benefit_courses.dao.count(self.benefit_courses.dao.table.c.benefit_id == benefit_id):
            raise HTTPException(409, "Remove this benefit's course bindings before deleting it.")
        self.benefits.dao.delete(benefit_id)
        self.db.commit()

    def list_plan_benefits(self, plan_id):
        self.plans.require(plan_id)
        return {"items": self.plan_benefits.list_for_plan(plan_id)}

    def replace_plan_benefits(self, plan_id, payload: s.MembershipPlanBenefitsInput, actor):
        self.plans.require(plan_id)
        benefit_ids = [item.benefit_id for item in payload.items]
        if len(benefit_ids) != len(set(benefit_ids)):
            raise HTTPException(422, "Each benefit can be configured only once per membership plan.")
        benefits = {benefit_id: self.benefits.require(benefit_id) for benefit_id in benefit_ids}
        rows = []
        for item in payload.items:
            benefit = benefits[item.benefit_id]
            self._validate_value(item.grant_value, benefit["value_type"], "grant_value")
            rows.append(
                {
                    "membership_plan_id": plan_id,
                    "benefit_id": item.benefit_id,
                    "grant_value_json": self._encode_json(item.grant_value, "grant_value"),
                    "is_enabled": int(item.is_enabled),
                    "sort_order": item.sort_order,
                    "created_by": actor["id"],
                    "updated_by": actor["id"],
                }
            )
        self.plan_benefits.dao.delete_where(self.plan_benefits.dao.table.c.membership_plan_id == plan_id)
        for row in rows:
            self.plan_benefits.dao.insert(row)
        self.db.commit()
        return self.list_plan_benefits(plan_id)

    def list_benefit_courses(self, benefit_id):
        self.benefits.require(benefit_id)
        return {"items": self.benefit_courses.list_for_benefit(benefit_id)}

    def replace_benefit_courses(self, benefit_id, payload: s.MembershipBenefitCoursesInput, actor):
        self.benefits.require(benefit_id)
        keys = [(item.course_id, item.access_action) for item in payload.items]
        if len(keys) != len(set(keys)):
            raise HTTPException(422, "A course and access action can be bound only once per benefit.")
        rows = []
        for item in payload.items:
            course = self.courses.require_any(item.course_id)
            if course["access_policy"] != "benefit":
                raise HTTPException(422, "Set the course access_policy to benefit before binding it.")
            rows.append(
                {
                    "benefit_id": benefit_id,
                    "course_id": item.course_id,
                    "access_action": item.access_action,
                    "is_enabled": int(item.is_enabled),
                    "sort_order": item.sort_order,
                    "created_by": actor["id"],
                    "updated_by": actor["id"],
                }
            )
        self.benefit_courses.dao.delete_where(self.benefit_courses.dao.table.c.benefit_id == benefit_id)
        for row in rows:
            self.benefit_courses.dao.insert(row)
        self.db.commit()
        return self.list_benefit_courses(benefit_id)

    def list_user_memberships(self, user_id):
        if not self.users.get(user_id):
            raise HTTPException(404, "User not found.")
        return {"items": self.user_memberships.list_for_user(user_id)}

    def list_admin_user_memberships(
        self,
        q="",
        membership_plan_id=None,
        status=None,
        source=None,
        page=1,
        page_size=20,
    ):
        result = self.user_memberships.dao.list_admin(
            q,
            membership_plan_id,
            status,
            source,
            page,
            page_size,
        )
        return {**result, "items": [serialise_membership(row) for row in result["items"]]}

    def save_user_membership(self, user_id, payload: s.UserMembershipInput, actor, membership_id=None):
        if not self.users.get(user_id):
            raise HTTPException(404, "User not found.")
        plan = self.plans.require(payload.membership_plan_id)
        if payload.status in {"pending", "active"} and plan["status"] != "active":
            raise HTTPException(409, "只能发放已启用的会员等级，请先在“会员等级”中将该等级设为启用。")
        starts_at = self._naive_utc(payload.starts_at)
        ends_at = self._naive_utc(payload.ends_at)
        if ends_at is None and plan["duration_days"]:
            ends_at = starts_at + timedelta(days=plan["duration_days"])
        if ends_at is not None and ends_at <= starts_at:
            raise HTTPException(422, "ends_at must be after starts_at.")
        if membership_id is not None:
            existing = self.user_memberships.require(membership_id)
            if existing["user_id"] != user_id:
                raise HTTPException(404, "Membership record not found for this user.")
        if payload.status == "active" and self.user_memberships.dao.active_overlapping(
            user_id, starts_at, ends_at, membership_id
        ):
            raise HTTPException(409, "This user already has an overlapping active membership.")
        values = self._none_when_blank(
            payload.model_dump(),
            ("external_reference", "cancel_reason"),
        )
        values["starts_at"] = starts_at
        values["ends_at"] = ends_at
        if values["status"] in {"cancelled", "revoked"} and values["cancelled_at"] is None:
            values["cancelled_at"] = datetime.now()
        if membership_id is None:
            values["user_id"] = user_id
            values["granted_by"] = actor["id"]
            membership_id = self.user_memberships.dao.insert(values)
        else:
            values["granted_by"] = actor["id"]
            self.user_memberships.dao.update(membership_id, values)
        self.db.commit()
        return serialise_membership(self.user_memberships.require(membership_id))

    def enroll_course(self, user, course_id):
        return self.user_courses.enroll(user, course_id)

    def list_my_courses(self, user):
        return self.user_courses.list_for_user(user["id"])

    def archive_my_course(self, user, course_id):
        self.user_courses.archive(user["id"], course_id)

    def open_course(self, user, course_id):
        course = self.user_courses.courses.require_public(course_id)
        access = self.user_courses.course_access(user["id"], course)
        catalog = LearningCatalogService(self.db)

        if access["access_state"] == "available":
            self.user_courses.enroll(user, course_id)
            result = catalog.get_course(course_id, include_lesson_content=True)
            return {
                **result,
                **access,
                "preview_lesson_count": None,
                "requires_membership": course["access_policy"] == "benefit",
            }

        # A benefit course can be opened without a membership only as a
        # preview.  Locked lessons deliberately omit their source content so
        # this is enforced by the API as well as represented in the UI.
        if access["access_state"] == "locked":
            result = catalog.get_course(
                course_id,
                include_lesson_content=True,
                unlocked_lesson_count=FREE_PREVIEW_LESSON_COUNT,
            )
            result.pop("content", None)
            return {
                **result,
                "access_state": "preview",
                "membership_id": None,
                "preview_lesson_count": FREE_PREVIEW_LESSON_COUNT,
                "requires_membership": True,
            }

        raise HTTPException(404, "Learning course is unavailable.")
