"""DAOs for membership configuration, grants, and learner course selections."""

from datetime import datetime

from sqlalchemy import func, or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class MembershipPlanDAO(BaseTableDAO):
    table = m.membership_plan

    def list_plans(self, q="", status=None, page=1, page_size=20):
        conditions = []
        if q:
            conditions.append(
                or_(
                    self.table.c.plan_code.ilike(f"%{q}%"),
                    self.table.c.name.ilike(f"%{q}%"),
                    self.table.c.name_en.ilike(f"%{q}%"),
                    self.table.c.description.ilike(f"%{q}%"),
                )
            )
        if status:
            conditions.append(self.table.c.status == status)
        return self.paginate_where(
            *conditions,
            order_by=[self.table.c.sort_order, self.table.c.id],
            page=page,
            page_size=page_size,
        )

    def clear_default(self, except_plan_id=None):
        conditions = [self.table.c.is_default == 1]
        if except_plan_id is not None:
            conditions.append(self.table.c.id != except_plan_id)
        self.db.execute(
            self.table.update().where(*conditions).values(is_default=0, updated_at=func.now())
        )

    def active_default(self):
        return (
            self.db.execute(
                select(self.table)
                .where(self.table.c.is_default == 1, self.table.c.status == "active")
                .order_by(self.table.c.id)
                .limit(1)
            )
            .mappings()
            .first()
        )


class MembershipBenefitDAO(BaseTableDAO):
    table = m.membership_benefit

    def list_benefits(self, q="", status=None, benefit_type=None, page=1, page_size=20):
        conditions = []
        if q:
            conditions.append(
                or_(
                    self.table.c.benefit_code.ilike(f"%{q}%"),
                    self.table.c.name.ilike(f"%{q}%"),
                    self.table.c.name_en.ilike(f"%{q}%"),
                    self.table.c.description.ilike(f"%{q}%"),
                )
            )
        if status:
            conditions.append(self.table.c.status == status)
        if benefit_type:
            conditions.append(self.table.c.benefit_type == benefit_type)
        return self.paginate_where(
            *conditions,
            order_by=[self.table.c.sort_order, self.table.c.id],
            page=page,
            page_size=page_size,
        )


class MembershipPlanBenefitDAO(BaseTableDAO):
    table = m.membership_plan_benefit

    def list_for_plan(self, plan_id):
        benefit = m.membership_benefit
        return (
            self.db.execute(
                select(
                    self.table,
                    benefit.c.benefit_code,
                    benefit.c.name.label("benefit_name"),
                    benefit.c.benefit_type,
                    benefit.c.value_type,
                    benefit.c.unit,
                    benefit.c.default_value_json,
                    benefit.c.status.label("benefit_status"),
                )
                .join(benefit, benefit.c.id == self.table.c.benefit_id)
                .where(self.table.c.membership_plan_id == plan_id)
                .order_by(self.table.c.sort_order, self.table.c.id)
            )
            .mappings()
            .all()
        )

    def enabled_benefit_ids_for_plans(self, plan_ids, target_benefit_ids):
        if not plan_ids or not target_benefit_ids:
            return []
        benefit = m.membership_benefit
        return self.db.scalars(
            select(self.table.c.benefit_id)
            .join(benefit, benefit.c.id == self.table.c.benefit_id)
            .where(
                self.table.c.membership_plan_id.in_(plan_ids),
                self.table.c.benefit_id.in_(target_benefit_ids),
                self.table.c.is_enabled == 1,
                benefit.c.status == "active",
            )
            .distinct()
        ).all()


class UserMembershipDAO(BaseTableDAO):
    table = m.user_membership

    def list_admin(self, q="", membership_plan_id=None, status=None, source=None, page=1, page_size=20):
        plan = m.membership_plan
        user = m.user
        conditions = []
        if q:
            conditions.append(
                or_(
                    user.c.username.ilike(f"%{q}%"),
                    user.c.full_name.ilike(f"%{q}%"),
                    user.c.email.ilike(f"%{q}%"),
                    user.c.contact_number.ilike(f"%{q}%"),
                )
            )
        if membership_plan_id is not None:
            conditions.append(self.table.c.membership_plan_id == membership_plan_id)
        if status:
            conditions.append(self.table.c.status == status)
        if source:
            conditions.append(self.table.c.source == source)

        base = self.table.join(user, user.c.id == self.table.c.user_id).join(
            plan, plan.c.id == self.table.c.membership_plan_id
        )
        total = self.db.scalar(select(func.count()).select_from(base).where(*conditions))
        rows = (
            self.db.execute(
                select(
                    self.table,
                    user.c.username,
                    user.c.full_name,
                    user.c.email.label("user_email"),
                    user.c.contact_number,
                    plan.c.plan_code,
                    plan.c.name.label("plan_name"),
                    plan.c.name_en.label("plan_name_en"),
                    plan.c.tier_rank,
                )
                .select_from(base)
                .where(*conditions)
                .order_by(self.table.c.starts_at.desc(), self.table.c.id.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }

    def list_for_user(self, user_id):
        plan = m.membership_plan
        return (
            self.db.execute(
                select(
                    self.table,
                    plan.c.plan_code,
                    plan.c.name.label("plan_name"),
                    plan.c.name_en.label("plan_name_en"),
                    plan.c.tier_rank,
                )
                .join(plan, plan.c.id == self.table.c.membership_plan_id)
                .where(self.table.c.user_id == user_id)
                .order_by(self.table.c.starts_at.desc(), self.table.c.id.desc())
            )
            .mappings()
            .all()
        )

    def active_for_user(self, user_id, now=None, except_membership_id=None):
        now = now or datetime.now()
        conditions = [
            self.table.c.user_id == user_id,
            self.table.c.status == "active",
            self.table.c.starts_at <= now,
            or_(self.table.c.ends_at.is_(None), self.table.c.ends_at > now),
        ]
        if except_membership_id is not None:
            conditions.append(self.table.c.id != except_membership_id)
        return (
            self.db.execute(
                select(self.table)
                .where(*conditions)
                .order_by(self.table.c.starts_at.desc(), self.table.c.id.desc())
            )
            .mappings()
            .all()
        )

    def active_overlapping(self, user_id, starts_at, ends_at, except_membership_id=None):
        conditions = [
            self.table.c.user_id == user_id,
            self.table.c.status == "active",
            or_(self.table.c.ends_at.is_(None), self.table.c.ends_at > starts_at),
        ]
        if ends_at is not None:
            conditions.append(self.table.c.starts_at < ends_at)
        if except_membership_id is not None:
            conditions.append(self.table.c.id != except_membership_id)
        return (
            self.db.execute(select(self.table).where(*conditions).order_by(self.table.c.id))
            .mappings()
            .all()
        )


class MembershipBenefitCourseDAO(BaseTableDAO):
    table = m.membership_benefit_course

    def list_for_benefit(self, benefit_id):
        course = m.learning_course
        return (
            self.db.execute(
                select(
                    self.table,
                    course.c.course_code,
                    course.c.title.label("course_title"),
                    course.c.title_en.label("course_title_en"),
                    course.c.access_policy,
                )
                .join(course, course.c.id == self.table.c.course_id)
                .where(self.table.c.benefit_id == benefit_id)
                .order_by(self.table.c.sort_order, self.table.c.id)
            )
            .mappings()
            .all()
        )

    def enabled_benefit_ids_for_course(self, course_id, action="study"):
        return self.db.scalars(
            select(self.table.c.benefit_id).where(
                self.table.c.course_id == course_id,
                self.table.c.access_action == action,
                self.table.c.is_enabled == 1,
            )
        ).all()


class LearningUserCourseDAO(BaseTableDAO):
    table = m.learning_user_course

    def find_for_user_course(self, user_id, course_id):
        return (
            self.db.execute(
                select(self.table).where(
                    self.table.c.user_id == user_id,
                    self.table.c.course_id == course_id,
                )
            )
            .mappings()
            .first()
        )

    def list_for_user(self, user_id):
        course = m.learning_course
        return (
            self.db.execute(
                select(
                    self.table,
                    course.c.course_code,
                    course.c.title.label("course_title"),
                    course.c.title_en.label("course_title_en"),
                    course.c.summary.label("course_summary"),
                    course.c.cover_url.label("course_cover_url"),
                    course.c.access_policy,
                    course.c.is_published.label("course_is_published"),
                )
                .join(course, course.c.id == self.table.c.course_id)
                .where(self.table.c.user_id == user_id)
                .order_by(
                    self.table.c.status,
                    self.table.c.last_opened_at.desc(),
                    self.table.c.enrolled_at.desc(),
                    self.table.c.id.desc(),
                )
            )
            .mappings()
            .all()
        )


MEMBERSHIP_TABLE_DAO_TYPES = {
    m.membership_plan.name: MembershipPlanDAO,
    m.membership_benefit.name: MembershipBenefitDAO,
    m.membership_plan_benefit.name: MembershipPlanBenefitDAO,
    m.user_membership.name: UserMembershipDAO,
    m.membership_benefit_course.name: MembershipBenefitCourseDAO,
    m.learning_user_course.name: LearningUserCourseDAO,
}
