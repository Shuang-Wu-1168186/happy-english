"""HTTP controllers for learning content and study progress."""

from fastapi import APIRouter, Body, Query, Request, UploadFile

from app.api.dependencies import Admin, Db, User
from app.services.content import ContentService
from app.services.media import ImageUploadService
from app.services.membership import MembershipService

router = APIRouter(tags=["learning"])


@router.get("/modules")
def modules(db: Db, user: User):
    return ContentService(db).module_counts()


@router.get("/content/{resource}")
def list_content(
    resource: str,
    db: Db,
    user: User,
    q: str = Query("", max_length=200),
    category: str = Query("", max_length=200),
    parent_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    language_register: str = Query("", max_length=32),
    scenario: str = Query("", max_length=40),
):
    MembershipService(db).require_legacy_content_access(user, resource)
    return ContentService(db).list_content(
        resource,
        q,
        category,
        parent_id,
        page,
        page_size,
        language_register,
        scenario,
    )


@router.get("/content/{resource}/{item_id}")
def get_content(resource: str, item_id: int, db: Db, user: User):
    MembershipService(db).require_legacy_content_access(user, resource)
    return ContentService(db).get_content(resource, item_id)


@router.post("/content/{resource}", status_code=201)
def create_content(resource: str, db: Db, admin: Admin, payload: dict = Body(...)):
    return ContentService(db).save(resource, payload, admin)


@router.put("/content/{resource}/{item_id}")
def update_content(resource: str, item_id: int, db: Db, admin: Admin, payload: dict = Body(...)):
    return ContentService(db).save(resource, payload, admin, item_id)


@router.delete("/content/{resource}/{item_id}", status_code=204)
def delete_content(resource: str, item_id: int, db: Db, admin: Admin):
    ContentService(db).delete(resource, item_id)


@router.post("/uploads", status_code=201)
def upload_image(request: Request, file: UploadFile, admin: Admin):
    return ImageUploadService(request.app.state.settings.uploads_dir).save(file)
