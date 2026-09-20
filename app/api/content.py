from io import BytesIO
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Query, Request, UploadFile
from PIL import Image, UnidentifiedImageError
from pydantic import ValidationError
from sqlalchemy import func, select

from app import models as m, schemas as s
from app.api.dependencies import Admin, Db, User
from app.repositories.content import ContentRepository, RESOURCES, table_for, visible

router = APIRouter(tags=["learning"])
INPUTS = {
    "sentences": s.SentenceInput,
    "notes": s.NoteInput,
    "note-items": s.NoteItemInput,
    "vocabulary": s.VocabularyInput,
    "interviews": s.InterviewInput,
}


@router.get("/modules")
def modules(db: Db, user: User):
    return {
        key: db.scalar(select(func.count()).select_from(table).where(*visible(table)))
        for key, table in RESOURCES.items()
    }


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
):
    return ContentRepository(db).list(resource, q, category, parent_id, page, page_size)


@router.get("/content/{resource}/{item_id}")
def get_content(resource: str, item_id: int, db: Db, user: User):
    return ContentRepository(db).get(resource, item_id)


def save(resource, payload, db, admin, item_id=None):
    schema = INPUTS.get(resource)
    if not schema:
        raise HTTPException(405, "This module is maintained through SQL imports.")
    try:
        values = schema.model_validate(payload).model_dump()
    except ValidationError as exc:
        raise HTTPException(422, exc.errors(include_context=False)) from exc
    sections = values.pop("sections", None)
    repo = ContentRepository(db)
    if resource == "note-items":
        repo.get("notes", values["note_id"])
    if resource == "interviews":
        repo.get("interview-categories", values["category_id"])
    table = table_for(resource)
    if item_id is None:
        if "created_by" in table.c:
            values["created_by"] = admin["id"]
        result = db.execute(table.insert().values(**values))
        item_id = result.inserted_primary_key[0]
    else:
        repo.get(resource, item_id)
        if "updated_by" in table.c:
            values["updated_by"] = admin["id"]
        db.execute(table.update().where(table.c.id == item_id).values(**values, updated_at=func.now()))
    if sections is not None:
        db.execute(
            m.interview_answer_section.delete().where(m.interview_answer_section.c.question_id == item_id)
        )
        for order, section in enumerate(sections):
            db.execute(
                m.interview_answer_section.insert().values(
                    **section, question_id=item_id, sort_order=order, created_by=admin["id"]
                )
            )
    db.commit()
    return repo.get(resource, item_id)


@router.post("/content/{resource}", status_code=201)
def create_content(resource: str, db: Db, admin: Admin, payload: dict = Body(...)):
    return save(resource, payload, db, admin)


@router.put("/content/{resource}/{item_id}")
def update_content(resource: str, item_id: int, db: Db, admin: Admin, payload: dict = Body(...)):
    return save(resource, payload, db, admin, item_id)


@router.delete("/content/{resource}/{item_id}", status_code=204)
def delete_content(resource: str, item_id: int, db: Db, admin: Admin):
    if resource not in INPUTS:
        raise HTTPException(405, "This module is maintained through SQL imports.")
    ContentRepository(db).get(resource, item_id)
    if resource == "notes":
        db.execute(
            m.study_progress.delete().where(
                m.study_progress.c.content_type == "english_note", m.study_progress.c.parent_id == item_id
            )
        )
        db.execute(m.english_note_item.delete().where(m.english_note_item.c.note_id == item_id))
    if resource in {"sentences", "note-items"}:
        kind = "everyday_sentence" if resource == "sentences" else "english_note"
        db.execute(
            m.study_progress.delete().where(
                m.study_progress.c.content_type == kind, m.study_progress.c.item_id == item_id
            )
        )
    if resource == "interviews":
        for child in (m.interview_answer_section, m.interview_question_tag):
            db.execute(child.delete().where(child.c.question_id == item_id))
    table = table_for(resource)
    db.execute(table.delete().where(table.c.id == item_id))
    db.commit()


@router.get("/progress")
def progress(db: Db, user: User):
    return (
        db.execute(
            select(m.study_progress)
            .where(m.study_progress.c.user_id == user["id"])
            .order_by(m.study_progress.c.last_studied_at.desc())
        )
        .mappings()
        .all()
    )


@router.post("/progress")
def save_progress(data: s.ProgressInput, db: Db, user: User):
    repo = ContentRepository(db)
    if data.content_type == "english_note":
        item = repo.get("note-items", data.item_id)
        repo.get("notes", data.parent_id)
        if item["note_id"] != data.parent_id:
            raise HTTPException(400, "This card does not belong to the selected note.")
    else:
        repo.get("sentences", data.item_id)
        data.parent_id = 0
    table = m.study_progress
    values = data.model_dump()
    values.update(user_id=user["id"], completed=int(data.completed))
    # Dialect upserts keep one bookmark per user/module even when two tabs save together.
    dialect = db.get_bind().dialect.name
    if dialect == "mysql":
        from sqlalchemy.dialects.mysql import insert

        stmt = insert(table).values(**values)
        stmt = stmt.on_duplicate_key_update(
            item_id=data.item_id,
            completed=int(data.completed),
            last_studied_at=func.now(),
            updated_at=func.now(),
        )
    else:
        from sqlalchemy.dialects.sqlite import insert

        stmt = (
            insert(table)
            .values(**values)
            .on_conflict_do_update(
                index_elements=["user_id", "content_type", "parent_id"],
                set_={
                    "item_id": data.item_id,
                    "completed": int(data.completed),
                    "last_studied_at": func.now(),
                    "updated_at": func.now(),
                },
            )
        )
    db.execute(stmt)
    db.commit()
    return {"success": True}


@router.post("/uploads", status_code=201)
def upload_image(request: Request, file: UploadFile, admin: Admin):
    data = file.file.read(5 * 1024 * 1024 + 1)
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(413, "Image must be smaller than 5 MB.")
    try:
        with Image.open(BytesIO(data)) as image:
            if image.width * image.height > 25_000_000:
                raise HTTPException(413, "Image dimensions are too large.")
            image.load()
            name = f"{uuid4().hex}.webp"
            image.convert("RGB").save(request.app.state.settings.uploads_dir / name, "WEBP")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise HTTPException(400, "Upload a valid image.") from exc
    return {"url": f"/static/uploads/{name}"}
