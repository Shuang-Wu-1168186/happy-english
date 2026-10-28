"""HTTP controllers for learning content and study progress."""

from fastapi import APIRouter, Body, Query, Request, UploadFile

from app import schemas as s
from app.api.dependencies import Admin, Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.services.content import ContentService
from app.services.media import ImageUploadService
from app.services.membership import MembershipService
from app.services.note_frequency import NoteItemFrequencyService

router = APIRouter(tags=["learning"], route_class=OpaqueIdRoute)


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
        user,
    )


@router.get("/content/{resource}/{item_id}")
def get_content(resource: str, item_id: int, db: Db, user: User):
    MembershipService(db).require_legacy_content_access(user, resource)
    return ContentService(db).get_content(resource, item_id, user)


@router.post("/content/note-items/{item_id}/frequency")
def increment_note_item_frequency(item_id: int, db: Db, user: User):
    MembershipService(db).require_legacy_content_access(user, "note-items")
    # Administrators can preview unpublished cards in the learning/search
    # screen, so use the same visibility rules as the list/detail endpoints.
    is_admin = bool(user and user.get("role") == "admin")
    ContentService(db).resource_service("note-items").require(item_id, admin=is_admin)
    frequency_count = NoteItemFrequencyService(db).increment(user["id"], item_id)
    db.commit()
    return {"success": True, "item_id": item_id, "frequency_count": frequency_count}


@router.patch("/content/note-items/{item_id}/language-register")
def update_note_item_language_register(
    item_id: int,
    payload: s.NoteItemLanguageRegisterInput,
    db: Db,
    admin: Admin,
):
    return ContentService(db).update_note_item_language_register(
        item_id, payload.language_register, admin
    )


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
