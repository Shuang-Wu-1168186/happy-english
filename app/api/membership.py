"""HTTP controllers for membership configuration and learner course access."""

from fastapi import APIRouter, Query

from app.api.dependencies import Admin, Db, User
from app.schemas import (
    LearningUserCourseInput,
    MembershipBenefitCoursesInput,
    MembershipBenefitInput,
    MembershipPlanBenefitsInput,
    MembershipPlanInput,
    UserMembershipInput,
)
from app.services.membership import MembershipService

router = APIRouter(tags=["membership"])


@router.get("/admin/membership-plans")
def list_membership_plans(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    status: str | None = Query(default=None, pattern="^(draft|active|inactive|archived)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return MembershipService(db).list_plans(q, status, page, page_size)


@router.post("/admin/membership-plans", status_code=201)
def create_membership_plan(payload: MembershipPlanInput, db: Db, admin: Admin):
    return MembershipService(db).save_plan(payload, admin)


@router.get("/admin/membership-plans/{plan_id}")
def get_membership_plan(plan_id: int, db: Db, admin: Admin):
    return MembershipService(db).get_plan(plan_id)


@router.put("/admin/membership-plans/{plan_id}")
def update_membership_plan(plan_id: int, payload: MembershipPlanInput, db: Db, admin: Admin):
    return MembershipService(db).save_plan(payload, admin, plan_id)


@router.delete("/admin/membership-plans/{plan_id}", status_code=204)
def delete_membership_plan(plan_id: int, db: Db, admin: Admin):
    MembershipService(db).delete_plan(plan_id)


@router.get("/admin/membership-plans/{plan_id}/benefits")
def list_plan_benefits(plan_id: int, db: Db, admin: Admin):
    return MembershipService(db).list_plan_benefits(plan_id)


@router.put("/admin/membership-plans/{plan_id}/benefits")
def replace_plan_benefits(
    plan_id: int,
    payload: MembershipPlanBenefitsInput,
    db: Db,
    admin: Admin,
):
    return MembershipService(db).replace_plan_benefits(plan_id, payload, admin)


@router.get("/admin/membership-benefits")
def list_membership_benefits(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    status: str | None = Query(default=None, pattern="^(active|inactive|archived)$"),
    benefit_type: str | None = Query(
        default=None,
        pattern="^(content_access|feature_access|quota|discount|service)$",
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return MembershipService(db).list_benefits(q, status, benefit_type, page, page_size)


@router.post("/admin/membership-benefits", status_code=201)
def create_membership_benefit(payload: MembershipBenefitInput, db: Db, admin: Admin):
    return MembershipService(db).save_benefit(payload, admin)


@router.get("/admin/membership-benefits/{benefit_id}")
def get_membership_benefit(benefit_id: int, db: Db, admin: Admin):
    return MembershipService(db).get_benefit(benefit_id)


@router.put("/admin/membership-benefits/{benefit_id}")
def update_membership_benefit(
    benefit_id: int,
    payload: MembershipBenefitInput,
    db: Db,
    admin: Admin,
):
    return MembershipService(db).save_benefit(payload, admin, benefit_id)


@router.delete("/admin/membership-benefits/{benefit_id}", status_code=204)
def delete_membership_benefit(benefit_id: int, db: Db, admin: Admin):
    MembershipService(db).delete_benefit(benefit_id)


@router.get("/admin/membership-benefits/{benefit_id}/courses")
def list_benefit_courses(benefit_id: int, db: Db, admin: Admin):
    return MembershipService(db).list_benefit_courses(benefit_id)


@router.put("/admin/membership-benefits/{benefit_id}/courses")
def replace_benefit_courses(
    benefit_id: int,
    payload: MembershipBenefitCoursesInput,
    db: Db,
    admin: Admin,
):
    return MembershipService(db).replace_benefit_courses(benefit_id, payload, admin)


@router.get("/admin/users/{user_id}/memberships")
def list_user_memberships(user_id: int, db: Db, admin: Admin):
    return MembershipService(db).list_user_memberships(user_id)


@router.get("/admin/user-memberships")
def list_admin_user_memberships(
    db: Db,
    admin: Admin,
    q: str = Query(default="", max_length=200),
    membership_plan_id: int | None = Query(default=None, gt=0),
    status: str | None = Query(default=None, pattern="^(pending|active|expired|cancelled|revoked)$"),
    source: str | None = Query(default=None, pattern="^(manual|purchase|trial|gift|migration|signup)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    return MembershipService(db).list_admin_user_memberships(
        q,
        membership_plan_id,
        status,
        source,
        page,
        page_size,
    )


@router.post("/admin/users/{user_id}/memberships", status_code=201)
def create_user_membership(user_id: int, payload: UserMembershipInput, db: Db, admin: Admin):
    return MembershipService(db).save_user_membership(user_id, payload, admin)


@router.put("/admin/users/{user_id}/memberships/{membership_id}")
def update_user_membership(
    user_id: int,
    membership_id: int,
    payload: UserMembershipInput,
    db: Db,
    admin: Admin,
):
    return MembershipService(db).save_user_membership(user_id, payload, admin, membership_id)


@router.get("/learning/memberships")
def my_memberships(db: Db, user: User):
    return MembershipService(db).list_user_memberships(user["id"])


@router.get("/learning/my-courses")
def my_courses(db: Db, user: User):
    return MembershipService(db).list_my_courses(user)


@router.post("/learning/my-courses", status_code=201)
def enroll_course(payload: LearningUserCourseInput, db: Db, user: User):
    return MembershipService(db).enroll_course(user, payload.course_id)


@router.delete("/learning/my-courses/{course_id}", status_code=204)
def archive_course(course_id: int, db: Db, user: User):
    MembershipService(db).archive_my_course(user, course_id)


@router.post("/learning/courses/{course_id}/open")
def open_course(course_id: int, db: Db, user: User):
    return MembershipService(db).open_course(user, course_id)
