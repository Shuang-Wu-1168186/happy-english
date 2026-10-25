"""HTTP controllers for private learning spaces and family sharing."""

from fastapi import APIRouter

from app.api.dependencies import Admin, Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.schemas import (
    FamilyGroupInput,
    FamilyGroupJoinInput,
    FamilyGroupMemberInput,
    PrivateZoneFeatureInput,
    PrivateZoneItemInput,
    PrivateZoneNoteInput,
    PrivateZoneNoteItemInput,
    PrivateZoneShortcutInput,
    PersonalNoteInput,
)
from app.services.private_zone import FamilyGroupService, PrivateZoneFeatureService, PrivateZoneService


router = APIRouter(tags=["private-zone"], route_class=OpaqueIdRoute)


@router.get("/learning/private-zone")
def private_zone_home(db: Db, user: User):
    return PrivateZoneService(db).home(user)


@router.get("/learning/private-zone/favorite-courses")
def list_private_zone_favorite_courses(db: Db, user: User):
    return PrivateZoneService(db).list_favorite_courses(user)


@router.get("/learning/private-zone/shortcuts")
def list_private_zone_shortcuts(db: Db, user: User):
    return PrivateZoneService(db).list_shortcuts(user)


@router.get("/learning/private-zone/personal-notes")
def list_personal_notes(db: Db, user: User):
    return PrivateZoneService(db).list_personal_notes(user)


@router.post("/learning/private-zone/personal-notes", status_code=201)
def create_personal_note(payload: PersonalNoteInput, db: Db, user: User):
    return PrivateZoneService(db).create_personal_note(payload, user)


@router.get("/learning/private-zone/personal-notes/{note_id}")
def get_personal_note(note_id: int, db: Db, user: User):
    return PrivateZoneService(db).get_personal_note(note_id, user)


@router.put("/learning/private-zone/personal-notes/{note_id}")
def update_personal_note(
    note_id: int, payload: PersonalNoteInput, db: Db, user: User
):
    return PrivateZoneService(db).update_personal_note(note_id, payload, user)


@router.delete("/learning/private-zone/personal-notes/{note_id}", status_code=204)
def delete_personal_note(note_id: int, db: Db, user: User):
    PrivateZoneService(db).delete_personal_note(note_id, user)


@router.get("/learning/private-zone/items")
def list_private_zone_items(db: Db, user: User):
    return PrivateZoneService(db).list_items(user)


@router.post("/learning/private-zone/items", status_code=201)
def add_private_zone_item(payload: PrivateZoneItemInput, db: Db, user: User):
    return PrivateZoneService(db).add_item(payload, user)


@router.delete("/learning/private-zone/items/{item_id}", status_code=204)
def remove_private_zone_item(item_id: int, db: Db, user: User):
    PrivateZoneService(db).remove_item(item_id, user)


@router.get("/learning/private-zone/notes")
def list_private_notes(db: Db, user: User):
    return PrivateZoneService(db).list_notes(user)


@router.post("/learning/private-zone/notes", status_code=201)
def create_private_note(payload: PrivateZoneNoteInput, db: Db, user: User):
    return PrivateZoneService(db).create_note(payload, user)


@router.post("/learning/private-zone/notes/{note_id}/items", status_code=201)
def create_private_note_item(
    note_id: int,
    payload: PrivateZoneNoteItemInput,
    db: Db,
    user: User,
):
    return PrivateZoneService(db).create_note_item(note_id, payload, user)


@router.delete("/learning/private-zone/notes/{note_id}", status_code=204)
def delete_private_note(note_id: int, db: Db, user: User):
    PrivateZoneService(db).delete_note(note_id, user)


@router.get("/learning/family-groups")
def list_family_groups(db: Db, user: User):
    return FamilyGroupService(db).list_for_user(user["id"])


@router.post("/learning/family-groups", status_code=201)
def create_family_group(payload: FamilyGroupInput, db: Db, user: User):
    return FamilyGroupService(db).create(payload, user)


@router.post("/learning/family-groups/join")
def join_family_group(payload: FamilyGroupJoinInput, db: Db, user: User):
    return FamilyGroupService(db).join_with_invite_code(payload, user)


@router.post("/learning/family-groups/{group_id}/invite-code")
def issue_family_group_invite_code(group_id: int, db: Db, user: User):
    return FamilyGroupService(db).issue_invite_code(group_id, user)


@router.get("/learning/family-groups/{group_id}/shortcuts")
def list_family_group_shortcuts(group_id: int, db: Db, user: User):
    return PrivateZoneService(db).list_family_shortcuts(group_id, user)


@router.post("/learning/family-groups/{group_id}/shortcuts", status_code=201)
def create_family_group_shortcut(
    group_id: int,
    payload: PrivateZoneShortcutInput,
    db: Db,
    user: User,
):
    return PrivateZoneService(db).create_family_shortcut(group_id, payload, user)


@router.put("/learning/family-groups/{group_id}/shortcuts/{shortcut_id}")
def update_family_group_shortcut(
    group_id: int,
    shortcut_id: int,
    payload: PrivateZoneShortcutInput,
    db: Db,
    user: User,
):
    return PrivateZoneService(db).update_family_shortcut(
        group_id, shortcut_id, payload, user
    )


@router.delete("/learning/family-groups/{group_id}/shortcuts/{shortcut_id}", status_code=204)
def delete_family_group_shortcut(group_id: int, shortcut_id: int, db: Db, user: User):
    PrivateZoneService(db).delete_family_shortcut(group_id, shortcut_id, user)


@router.put("/learning/family-groups/{group_id}")
def rename_family_group(group_id: int, payload: FamilyGroupInput, db: Db, user: User):
    return FamilyGroupService(db).rename(group_id, payload, user)


@router.post("/learning/family-groups/{group_id}/members")
def add_family_member(
    group_id: int,
    payload: FamilyGroupMemberInput,
    db: Db,
    user: User,
):
    return FamilyGroupService(db).add_member(group_id, payload, user)


@router.delete("/learning/family-groups/{group_id}/members/{target_user_id}", status_code=204)
def remove_family_member(group_id: int, target_user_id: int, db: Db, user: User):
    FamilyGroupService(db).remove_member(group_id, target_user_id, user)


@router.get("/admin/private-zone/features")
def list_private_zone_features(db: Db, admin: Admin):
    return {"items": PrivateZoneFeatureService(db).list(enabled_only=False)}


@router.post("/admin/private-zone/features", status_code=201)
def create_private_zone_feature(
    payload: PrivateZoneFeatureInput,
    db: Db,
    admin: Admin,
):
    return PrivateZoneFeatureService(db).create_public_entry(payload, admin)


@router.put("/admin/private-zone/features/{feature_code}")
def save_private_zone_feature(
    feature_code: str,
    payload: PrivateZoneFeatureInput,
    db: Db,
    admin: Admin,
):
    return PrivateZoneFeatureService(db).save(feature_code, payload, admin)


@router.get("/admin/private-zone/shortcuts")
def list_admin_private_zone_shortcuts(db: Db, admin: Admin):
    return PrivateZoneService(db).list_admin_shortcuts(admin)


@router.post("/admin/private-zone/shortcuts", status_code=201)
def create_admin_private_zone_shortcut(
    payload: PrivateZoneShortcutInput, db: Db, admin: Admin
):
    return PrivateZoneService(db).create_admin_shortcut(payload, admin)


@router.put("/admin/private-zone/shortcuts/{shortcut_id}")
def update_admin_private_zone_shortcut(
    shortcut_id: int,
    payload: PrivateZoneShortcutInput,
    db: Db,
    admin: Admin,
):
    return PrivateZoneService(db).update_admin_shortcut(shortcut_id, payload, admin)


@router.delete("/admin/private-zone/shortcuts/{shortcut_id}", status_code=204)
def delete_admin_private_zone_shortcut(shortcut_id: int, db: Db, admin: Admin):
    PrivateZoneService(db).delete_admin_shortcut(shortcut_id, admin)
