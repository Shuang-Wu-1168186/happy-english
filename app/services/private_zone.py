"""Private learning-zone, family-sharing, and scoped-note business rules."""

import json
import re
import secrets
from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import and_, or_, select

from app import models as m
from app import schemas as s
from app.dao.accounts import UserDAO
from app.dao.content import EnglishNoteDAO, EnglishNoteItemDAO
from app.dao.learning_catalog import LearningCourseDAO, LearningMaterialDAO
from app.dao.private_zone import (
    FamilyGroupDAO,
    FamilyGroupMemberDAO,
    PersonalNoteDAO,
    PrivateZoneFeatureDAO,
    PrivateZoneItemDAO,
    PrivateZoneShortcutDAO,
)
from app.services.content import serialise_content
from app.services.membership import LearningUserCourseService


DEFAULT_PRIVATE_ZONE_FEATURES = (
    {
        "feature_code": "my-english-notes",
        "title": "我的英语笔记",
        "title_en": "My English Notes",
        "description": "整理个人笔记、家庭共学笔记和复习内容。",
        "icon": "notebook",
        "route_key": "private-notes",
        "target_url": "/learn/notes",
        "config": {"resource_types": ["note", "note_item"]},
        "sort_order": 10,
    },
    {
        "feature_code": "my-textbooks",
        "title": "我的课本",
        "title_en": "My Textbooks",
        "description": "收藏课本、教材和按单元组织的学习材料。",
        "icon": "book-open",
        "route_key": "private-textbooks",
        "target_url": "/learning-materials/1",
        "config": {
            "resource_types": ["material"],
            "material_types": ["textbook", "book", "courseware"],
        },
        "sort_order": 20,
    },
    {
        "feature_code": "textbook-vocabulary",
        "title": "课本单词",
        "title_en": "Textbook Vocabulary",
        "description": "收藏课本单词、词卡和复习词表。",
        "icon": "languages",
        "route_key": "textbook-vocabulary",
        "target_url": "/learn/kids-cards",
        "config": {
            "resource_types": ["material"],
            "material_types": ["card_set", "cards"],
            "material_code_prefixes": ["kids-cards-"],
        },
        "sort_order": 30,
    },
    {
        "feature_code": "my-interview-questions",
        "title": "我的面试题",
        "title_en": "My Interview Practice",
        "description": "收藏常见面试题、技术面试题和回答练习。",
        "icon": "briefcase",
        "route_key": "private-interviews",
        "target_url": "/learn/interviews",
        "config": {
            "resource_types": ["material"],
            "material_types": ["interview"],
        },
        "sort_order": 35,
    },
    {
        "feature_code": "saved-learning",
        "title": "我的学习内容",
        "title_en": "Saved Learning",
        "description": "收藏课程和其他可复用的学习材料。",
        "icon": "bookmark",
        "route_key": "saved-learning",
        "target_url": "/private-zone/favorite-courses",
        "config": {"resource_types": ["course", "material"]},
        "sort_order": 40,
        "is_enabled": 0,
    },
)

# Keep the configured public entries for a later product decision, but do not
# expose them to learners while the feature is paused.
PRIVATE_ZONE_PUBLIC_ENTRIES_ENABLED = False

FAMILY_INVITE_LIFETIME = timedelta(days=7)
FAMILY_INVITE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _decode_json(value, fallback):
    if value is None:
        return fallback
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return fallback


def serialise_private_feature(row):
    result = dict(row)
    result["config"] = _decode_json(result.pop("config_json", None), {})
    return result


def _public_user(row):
    return {
        key: row[key]
        for key in ("id", "username", "full_name", "email")
        if key in row
    }


class FamilyGroupService:
    """Manage active family groups and their memberships."""

    def __init__(self, db):
        self.db = db
        self.groups = FamilyGroupDAO(db)
        self.members = FamilyGroupMemberDAO(db)
        self.users = UserDAO(db)

    def require_group(self, group_id):
        row = self.groups.find_by_id(group_id)
        if not row or row["status"] != "active":
            raise HTTPException(404, "Family group not found.")
        return row

    def require_membership(self, group_id, user_id, *, roles=None):
        self.require_group(group_id)
        membership = self.members.find_membership(group_id, user_id, active_only=True)
        if not membership:
            raise HTTPException(403, "You are not an active member of this family group.")
        if roles and membership["role"] not in roles:
            raise HTTPException(403, "Only the family owner or an administrator can do this.")
        return membership

    def group_ids_for_user(self, user_id):
        return self.members.active_group_ids_for_user(user_id)

    def managed_group_ids_for_user(self, user_id):
        return [
            group["id"]
            for group in self.groups.list_for_user(user_id)
            if group["member_role"] in {"owner", "admin"}
        ]

    @staticmethod
    def _normalise_invite_code(invite_code):
        return re.sub(r"[^A-Z0-9]", "", (invite_code or "").upper())

    @staticmethod
    def _display_invite_code(invite_code):
        return "-".join(
            invite_code[index : index + 4]
            for index in range(0, len(invite_code), 4)
        )

    def _new_invite_code(self):
        for _ in range(20):
            code = "".join(secrets.choice(FAMILY_INVITE_ALPHABET) for _ in range(8))
            if not self.groups.by_invite_code(code):
                return code
        raise HTTPException(503, "Unable to create a family invite code. Please try again.")

    def _invite_payload(self, group):
        invite_code = group.get("invite_code")
        if not invite_code:
            return None
        return {
            "family_group_id": group["id"],
            "family_group_name": group["name"],
            "invite_code": self._display_invite_code(invite_code),
            "expires_at": group.get("invite_code_expires_at"),
        }

    def list_for_user(self, user_id):
        items = []
        for group in self.groups.list_for_user(user_id):
            members = [
                {
                    **dict(row),
                    "user": _public_user(row),
                }
                for row in self.members.list_for_group(group["id"])
            ]
            for member in members:
                for key in ("username", "full_name", "email"):
                    member.pop(key, None)
            items.append({**dict(group), "members": members})
        return {"items": items}

    def create(self, payload: s.FamilyGroupInput, user):
        group_id = self.groups.insert(
            {
                "name": payload.name,
                "owner_user_id": user["id"],
                "status": "active",
            }
        )
        self.members.insert(
            {
                "family_group_id": group_id,
                "user_id": user["id"],
                "role": "owner",
                "status": "active",
                "invited_by": user["id"],
                "joined_at": datetime.now(),
            }
        )
        self.db.commit()
        return self.get(group_id, user["id"])

    def issue_invite_code(self, group_id, user):
        self.require_membership(group_id, user["id"], roles={"owner", "admin"})
        group = self.require_group(group_id)
        now = datetime.now()
        expires_at = group.get("invite_code_expires_at")
        if group.get("invite_code") and expires_at and expires_at > now:
            return self._invite_payload(group)
        values = {
            "invite_code": self._new_invite_code(),
            "invite_code_expires_at": now + FAMILY_INVITE_LIFETIME,
        }
        self.groups.update(group_id, values)
        self.db.commit()
        return self._invite_payload(self.require_group(group_id))

    def join_with_invite_code(self, payload: s.FamilyGroupJoinInput, user):
        invite_code = self._normalise_invite_code(payload.invite_code)
        group = self.groups.by_invite_code(invite_code)
        if not group or group["status"] != "active":
            raise HTTPException(404, "Invite code not found.")
        expires_at = group.get("invite_code_expires_at")
        if not expires_at or expires_at <= datetime.now():
            raise HTTPException(410, "This invite code has expired. Ask the family owner for a new one.")
        existing = self.members.find_membership(group["id"], user["id"])
        if existing and existing["status"] == "active":
            raise HTTPException(409, "You are already in this family.")
        values = {
            "role": "member",
            "status": "active",
            "invited_by": group.get("owner_user_id"),
            "joined_at": datetime.now(),
        }
        if existing:
            self.members.update(existing["id"], values)
        else:
            self.members.insert(
                {
                    **values,
                    "family_group_id": group["id"],
                    "user_id": user["id"],
                }
            )
        self.db.commit()
        return self.get(group["id"], user["id"])

    def get(self, group_id, user_id):
        self.require_membership(group_id, user_id)
        group = self.require_group(group_id)
        members = []
        for row in self.members.list_for_group(group_id):
            member = dict(row)
            member["user"] = _public_user(row)
            for key in ("username", "full_name", "email"):
                member.pop(key, None)
            members.append(member)
        return {**dict(group), "members": members}

    def rename(self, group_id, payload: s.FamilyGroupInput, user):
        self.require_membership(group_id, user["id"], roles={"owner", "admin"})
        self.groups.update(group_id, {"name": payload.name})
        self.db.commit()
        return self.get(group_id, user["id"])

    def add_member(self, group_id, payload: s.FamilyGroupMemberInput, user):
        self.require_membership(group_id, user["id"], roles={"owner", "admin"})
        if payload.user_id:
            target = self.users.get(payload.user_id)
        elif payload.username:
            target = self.users.by_username(payload.username)
        else:
            raise HTTPException(422, "Enter a member username or user ID.")
        if not target or target["status"] != "active":
            raise HTTPException(404, "User not found or inactive.")
        target_user_id = target["id"]
        existing = self.members.find_membership(group_id, target_user_id)
        if existing and existing["status"] == "active":
            raise HTTPException(409, "This user is already an active family member.")
        values = {
            "role": payload.role,
            "status": "active",
            "invited_by": user["id"],
            "joined_at": datetime.now(),
        }
        if existing:
            self.members.update(existing["id"], values)
        else:
            self.members.insert(
                {
                    **values,
                    "family_group_id": group_id,
                    "user_id": target_user_id,
                }
            )
        self.db.commit()
        return self.get(group_id, user["id"])

    def remove_member(self, group_id, target_user_id, user):
        actor_membership = self.require_membership(group_id, user["id"])
        target = self.members.find_membership(group_id, target_user_id, active_only=True)
        if not target:
            raise HTTPException(404, "Active family member not found.")
        if target["role"] == "owner":
            raise HTTPException(409, "The family owner cannot be removed.")
        if target_user_id != user["id"] and actor_membership["role"] not in {"owner", "admin"}:
            raise HTTPException(403, "Only the family owner or an administrator can remove members.")
        self.members.update(target["id"], {"status": "left"})
        self.db.commit()


class FamilyGroupMemberService:
    """Table-level service registration for family_group_member."""

    dao_type = FamilyGroupMemberDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class PrivateZoneFeatureService:
    dao_type = PrivateZoneFeatureDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)

    def _ensure_defaults(self):
        changed = False
        for definition in DEFAULT_PRIVATE_ZONE_FEATURES:
            existing = self.dao.by_code(definition["feature_code"])
            if existing:
                # Older deployments predate the public target URL.  Fill only
                # an empty value so an administrator's deliberate change is
                # never overwritten by an application restart.
                if not existing.get("target_url"):
                    self.dao.update(
                        existing["id"], {"target_url": definition["target_url"]}
                    )
                    changed = True
                continue
            self.dao.insert(
                {
                    "feature_code": definition["feature_code"],
                    "title": definition["title"],
                    "title_en": definition["title_en"],
                    "description": definition["description"],
                    "icon": definition["icon"],
                    "route_key": definition["route_key"],
                    "target_url": definition["target_url"],
                    "config_json": json.dumps(definition["config"], ensure_ascii=False),
                    "sort_order": definition["sort_order"],
                    "is_enabled": definition.get("is_enabled", 1),
                }
            )
            changed = True
        if changed:
            self.db.commit()

    def list(self, enabled_only=False):
        self._ensure_defaults()
        return [
            serialise_private_feature(row)
            for row in self.dao.list_features(enabled_only=enabled_only)
        ]

    def list_public_entries(self):
        """Return only the learner-facing part of the public configuration."""
        fields = (
            "id",
            "feature_code",
            "title",
            "title_en",
            "description",
            "icon",
            "target_url",
            "sort_order",
        )
        return [
            {field: feature.get(field) for field in fields}
            for feature in self.list(enabled_only=True)
            if feature.get("target_url")
        ]

    def save(self, feature_code, payload: s.PrivateZoneFeatureInput, actor):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", feature_code):
            raise HTTPException(422, "Invalid private-zone feature code.")
        values = payload.model_dump()
        config = values.pop("config")
        for field in ("title_en", "description", "icon"):
            if values.get(field) == "":
                values[field] = None
        values["config_json"] = json.dumps(config or {}, ensure_ascii=False, separators=(",", ":"))
        values["updated_by"] = actor["id"]
        existing = self.dao.by_code(feature_code)
        if existing:
            self.dao.update(existing["id"], values)
            feature_id = existing["id"]
        else:
            values.update(feature_code=feature_code, created_by=actor["id"])
            feature_id = self.dao.insert(values)
        self.db.commit()
        return serialise_private_feature(self.dao.find_by_id(feature_id))

    def create_public_entry(self, payload: s.PrivateZoneFeatureInput, actor):
        """Create a public-only entry without making operators manage IDs."""
        for _ in range(20):
            feature_code = f"public-{secrets.token_hex(6)}"
            if not self.dao.by_code(feature_code):
                return self.save(feature_code, payload, actor)
        raise HTTPException(503, "Unable to create a public entry. Please try again.")


class PrivateZoneItemService:
    dao_type = PrivateZoneItemDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class PrivateZoneShortcutService:
    """Table-level service registration for learner-owned shortcuts."""

    dao_type = PrivateZoneShortcutDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class PersonalNoteService:
    """Table-level service registration for the standalone personal notebook."""

    dao_type = PersonalNoteDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


class PrivateZoneService:
    """Aggregate private-zone items without copying catalogue content."""

    def __init__(self, db):
        self.db = db
        self.family_groups = FamilyGroupService(db)
        self.features = PrivateZoneFeatureService(db)
        self.items = PrivateZoneItemService(db)
        self.shortcuts = PrivateZoneShortcutDAO(db)
        self.personal_notes = PersonalNoteDAO(db)
        self.users = UserDAO(db)
        self.notes = EnglishNoteDAO(db)
        self.note_items = EnglishNoteItemDAO(db)
        self.materials = LearningMaterialDAO(db)
        self.courses = LearningCourseDAO(db)
        self.user_courses = LearningUserCourseService(db)

    def _scope_values(self, scope_type, family_group_id, user_id):
        if scope_type == "personal":
            if family_group_id is not None:
                raise HTTPException(422, "A personal item cannot reference a family group.")
            return user_id, None
        if not family_group_id:
            raise HTTPException(422, "A family item must reference a family group.")
        self.family_groups.require_membership(family_group_id, user_id)
        return None, family_group_id

    def _note_scope_access(self, note, user_id, *, admin=False):
        scope_type = note.get("scope_type") or "platform"
        if scope_type == "platform":
            return admin or note.get("share_status") == 1
        if scope_type == "personal":
            return note.get("owner_user_id") == user_id
        if scope_type == "family":
            group_id = note.get("family_group_id")
            return bool(
                group_id
                and self.family_groups.members.find_membership(
                    group_id, user_id, active_only=True
                )
            )
        return False

    def _require_note_access(self, note_id, user, *, admin=False):
        note = self.notes.find_by_id(note_id)
        if not note or not self._note_scope_access(note, user["id"], admin=admin):
            raise HTTPException(404, "Private note not found.")
        return note

    def _resource(self, resource_type, resource_id, user):
        if resource_type == "material":
            row = self.materials.get_published(resource_id)
            if not row:
                raise HTTPException(404, "Learning material not found.")
            return {
                **dict(row),
                "resource_type": resource_type,
                "access": self.user_courses.material_access(user, resource_id),
            }
        if resource_type == "course":
            row = self.courses.get_published(resource_id)
            if not row:
                raise HTTPException(404, "Learning course not found.")
            return {
                **dict(row),
                "resource_type": resource_type,
                "access": self.user_courses.course_access(user, row),
            }
        if resource_type == "note":
            row = self._require_note_access(
                resource_id, user, admin=user.get("role") == "admin"
            )
            return {**serialise_content(row), "resource_type": resource_type}
        if resource_type == "note_item":
            row = self.note_items.find_by_id(resource_id)
            if not row:
                raise HTTPException(404, "Private note item not found.")
            note = self._require_note_access(
                row["note_id"], user, admin=user.get("role") == "admin"
            )
            return {
                **serialise_content(row),
                "resource_type": resource_type,
                "note_id": note["id"],
            }
        raise HTTPException(422, "Unsupported private-zone resource type.")

    def _feature_for_resource(self, resource_type, resource):
        material_type = resource.get("material_type")
        material_code = resource.get("material_code") or ""
        for feature in self.features.list(enabled_only=True):
            config = feature.get("config") or {}
            resource_types = config.get("resource_types") or []
            material_types = config.get("material_types") or []
            material_codes = config.get("material_codes") or []
            material_code_prefixes = config.get("material_code_prefixes") or []
            if resource_type not in resource_types:
                continue
            if material_types and material_type not in material_types:
                continue
            if material_codes and material_code not in material_codes:
                continue
            if material_code_prefixes and not any(
                material_code.startswith(prefix)
                for prefix in material_code_prefixes
                if isinstance(prefix, str)
            ):
                continue
            return feature
        return None

    def _item_view(self, item, user):
        resource = self._resource(item["resource_type"], item["resource_id"], user)
        feature = self._feature_for_resource(item["resource_type"], resource)
        group = None
        if item["scope_type"] == "family":
            group = self.family_groups.require_group(item["family_group_id"])
        access = resource.get("access", {"access_state": "available"})
        return {
            **dict(item),
            "source": {
                "scope_type": item["scope_type"],
                "label": "个人" if item["scope_type"] == "personal" else "家庭",
                "family_group_id": item["family_group_id"],
                "family_group_name": group["name"] if group else None,
            },
            "feature": feature,
            "resource": resource,
            "access": access,
        }

    def list_items(self, user):
        group_ids = self.family_groups.group_ids_for_user(user["id"])
        items = [
            self._item_view(item, user)
            for item in self.items.dao.list_for_user(user["id"], group_ids)
        ]
        return {"items": items}

    def list_favorite_courses(self, user):
        return {
            "items": [
                item
                for item in self.list_items(user)["items"]
                if item["resource_type"] == "course"
            ]
        }

    @staticmethod
    def _shortcut_values(payload):
        values = payload.model_dump()
        for field in ("description", "icon"):
            values[field] = values[field] or None
        return values

    @staticmethod
    def _personal_note_values(payload):
        values = payload.model_dump()
        for field in ("content", "tags", "color"):
            values[field] = values[field] or None
        return values

    def _shortcut_view(self, shortcut):
        result = dict(shortcut)
        family_group_id = result.get("family_group_id")
        family_group_name = result.get("family_group_name")
        if family_group_id and not family_group_name:
            family_group_name = self.family_groups.require_group(family_group_id)["name"]
        result["family_group_name"] = family_group_name
        result["source"] = {
            "scope_type": "family",
            "label": "来自家庭",
            "family_group_id": family_group_id,
            "family_group_name": family_group_name,
        }
        return result

    def _require_shortcut_family_manager(self, family_group_id, admin):
        if not family_group_id:
            raise HTTPException(404, "Shortcut family group not found.")
        self.family_groups.require_membership(
            family_group_id,
            admin["id"],
            roles={"owner", "admin"},
        )

    def _require_admin_shortcut(self, shortcut_id, admin):
        shortcut = self.shortcuts.find_active_for_user(shortcut_id, admin["id"])
        if not shortcut:
            raise HTTPException(404, "Shortcut not found.")
        self._require_shortcut_family_manager(shortcut["family_group_id"], admin)
        return shortcut

    def list_shortcuts(self, user):
        """List shortcuts shared by the signed-in user's active families."""
        group_ids = self.family_groups.group_ids_for_user(user["id"])
        return {
            "items": [
                self._shortcut_view(row)
                for row in self.shortcuts.list_for_family_members(group_ids)
            ]
        }

    def list_admin_shortcuts(self, admin):
        """List shortcuts this administrator owns in families they can manage."""
        group_ids = self.family_groups.managed_group_ids_for_user(admin["id"])
        return {
            "items": [
                self._shortcut_view(row)
                for row in self.shortcuts.list_for_owner_in_families(admin["id"], group_ids)
            ]
        }

    def create_admin_shortcut(self, payload: s.PrivateZoneShortcutInput, admin):
        self._require_shortcut_family_manager(payload.family_group_id, admin)
        shortcut_id = self.shortcuts.insert(
            {
                **self._shortcut_values(payload),
                "user_id": admin["id"],
                "scope_type": "family",
                "status": "active",
            }
        )
        self.db.commit()
        return self._shortcut_view(self.shortcuts.find_by_id(shortcut_id))

    def update_admin_shortcut(
        self, shortcut_id, payload: s.PrivateZoneShortcutInput, admin
    ):
        self._require_admin_shortcut(shortcut_id, admin)
        self._require_shortcut_family_manager(payload.family_group_id, admin)
        self.shortcuts.update(shortcut_id, self._shortcut_values(payload))
        self.db.commit()
        return self._shortcut_view(self.shortcuts.find_by_id(shortcut_id))

    def delete_admin_shortcut(self, shortcut_id, admin):
        self._require_admin_shortcut(shortcut_id, admin)
        self.shortcuts.update(shortcut_id, {"status": "archived"})
        self.db.commit()

    def _require_personal_note(self, note_id, user):
        note = self.personal_notes.find_active_for_user(note_id, user["id"])
        if not note:
            raise HTTPException(404, "Personal note not found.")
        return note

    def list_personal_notes(self, user):
        return {
            "items": [dict(row) for row in self.personal_notes.list_for_user(user["id"])]
        }

    def get_personal_note(self, note_id, user):
        return dict(self._require_personal_note(note_id, user))

    def create_personal_note(self, payload: s.PersonalNoteInput, user):
        note_id = self.personal_notes.insert(
            {**self._personal_note_values(payload), "user_id": user["id"], "status": "active"}
        )
        self.db.commit()
        return dict(self.personal_notes.find_by_id(note_id))

    def update_personal_note(self, note_id, payload: s.PersonalNoteInput, user):
        self._require_personal_note(note_id, user)
        self.personal_notes.update(note_id, self._personal_note_values(payload))
        self.db.commit()
        return dict(self.personal_notes.find_by_id(note_id))

    def delete_personal_note(self, note_id, user):
        self._require_personal_note(note_id, user)
        self.personal_notes.update(note_id, {"status": "archived"})
        self.db.commit()

    def home(self, user):
        items = self.list_items(user)["items"]
        personal_notes = self.list_personal_notes(user)["items"]
        return {
            "features": self.features.list(enabled_only=True),
            "public_entries": (
                self.features.list_public_entries()
                if PRIVATE_ZONE_PUBLIC_ENTRIES_ENABLED
                else []
            ),
            "family_groups": self.family_groups.list_for_user(user["id"])["items"],
            "items": items,
            "favorite_course_count": sum(
                item["resource_type"] == "course" for item in items
            ),
            "shortcuts": self.list_shortcuts(user)["items"],
            "personal_note_count": len(personal_notes),
            "recent_personal_notes": personal_notes[:3],
        }

    def add_item(self, payload: s.PrivateZoneItemInput, user):
        owner_user_id, family_group_id = self._scope_values(
            payload.scope_type, payload.family_group_id, user["id"]
        )
        self._resource(payload.resource_type, payload.resource_id, user)
        duplicate = self.items.dao.find_active_duplicate(
            payload.scope_type,
            owner_user_id,
            family_group_id,
            payload.resource_type,
            payload.resource_id,
        )
        if duplicate:
            raise HTTPException(409, "This content is already in the selected private scope.")
        item_id = self.items.dao.insert(
            {
                "scope_type": payload.scope_type,
                "owner_user_id": owner_user_id,
                "family_group_id": family_group_id,
                "resource_type": payload.resource_type,
                "resource_id": payload.resource_id,
                "label": payload.label or None,
                "sort_order": payload.sort_order,
                "status": "active",
                "added_by_user_id": user["id"],
            }
        )
        self.db.commit()
        return self._item_view(self.items.dao.find_by_id(item_id), user)

    def remove_item(self, item_id, user):
        item = self.items.dao.find_by_id(item_id)
        if not item or item["status"] != "active":
            raise HTTPException(404, "Private-zone item not found.")
        if item["scope_type"] == "personal":
            if item["owner_user_id"] != user["id"]:
                raise HTTPException(403, "You cannot remove another user's private item.")
        else:
            self.family_groups.require_membership(
                item["family_group_id"], user["id"], roles={"owner", "admin"}
            )
        self.items.dao.update(item_id, {"status": "archived"})
        self.db.commit()

    def create_note(self, payload: s.PrivateZoneNoteInput, user):
        owner_user_id, family_group_id = self._scope_values(
            payload.scope_type, payload.family_group_id, user["id"]
        )
        note_id = self.notes.insert(
            {
                "note_date": payload.note_date,
                "title": payload.title,
                "source": payload.source or None,
                "summary": payload.summary or None,
                "share_status": 0,
                "scope_type": payload.scope_type,
                "owner_user_id": owner_user_id,
                "family_group_id": family_group_id,
                "priority_order": payload.priority_order,
                "created_by": user["id"],
            }
        )
        item_id = self.items.dao.insert(
            {
                "scope_type": payload.scope_type,
                "owner_user_id": owner_user_id,
                "family_group_id": family_group_id,
                "resource_type": "note",
                "resource_id": note_id,
                "sort_order": payload.priority_order,
                "status": "active",
                "added_by_user_id": user["id"],
            }
        )
        self.db.commit()
        return {
            "note": serialise_content(self.notes.find_by_id(note_id)),
            "item": self._item_view(self.items.dao.find_by_id(item_id), user),
        }

    def list_notes(self, user):
        group_ids = self.family_groups.group_ids_for_user(user["id"])
        conditions = [
            or_(
                and_(
                    m.english_note.c.scope_type == "personal",
                    m.english_note.c.owner_user_id == user["id"],
                ),
                and_(
                    m.english_note.c.scope_type == "family",
                    m.english_note.c.family_group_id.in_(group_ids),
                ),
            )
        ]
        rows = self.db.execute(
            select(m.english_note).where(*conditions).order_by(
                m.english_note.c.note_date.desc(), m.english_note.c.id.desc()
            )
        ).mappings().all()
        return {"items": [serialise_content(row) for row in rows]}

    def create_note_item(self, note_id, payload: s.PrivateZoneNoteItemInput, user):
        note = self._require_note_access(note_id, user)
        if note.get("scope_type") not in {"personal", "family"}:
            raise HTTPException(422, "Only personal or family notes can be edited here.")
        values = payload.model_dump()
        values.update(
            {
                "note_id": note_id,
                "example_image_url": values["example_image_url"] or None,
                "example_image_alt": values["example_image_alt"] or None,
                "explanation": values["explanation"] or None,
                "examples": values["examples"] or None,
                "keywords": values["keywords"] or None,
                "share_status": 0,
                "created_by": user["id"],
            }
        )
        values.pop("priority_order")
        item_id = self.note_items.insert(values)
        duplicate = self.items.dao.find_active_duplicate(
            note["scope_type"],
            note["owner_user_id"],
            note["family_group_id"],
            "note_item",
            item_id,
        )
        if not duplicate:
            self.items.dao.insert(
                {
                    "scope_type": note["scope_type"],
                    "owner_user_id": note["owner_user_id"],
                    "family_group_id": note["family_group_id"],
                    "resource_type": "note_item",
                    "resource_id": item_id,
                    "sort_order": payload.priority_order,
                    "status": "active",
                    "added_by_user_id": user["id"],
                }
            )
        self.db.commit()
        return self._item_view(
            self.items.dao.find_active_duplicate(
                note["scope_type"],
                note["owner_user_id"],
                note["family_group_id"],
                "note_item",
                item_id,
            ),
            user,
        )

    def delete_note(self, note_id, user):
        note = self._require_note_access(note_id, user)
        if note.get("scope_type") == "family":
            self.family_groups.require_membership(
                note["family_group_id"], user["id"], roles={"owner", "admin"}
            )
        elif note.get("owner_user_id") != user["id"]:
            raise HTTPException(403, "You cannot delete another user's private note.")
        child_ids = select(m.english_note_item.c.id).where(
            m.english_note_item.c.note_id == note_id
        )
        self.items.dao.delete_where(
            self.items.dao.table.c.resource_type == "note_item",
            self.items.dao.table.c.resource_id.in_(child_ids),
        )
        self.items.dao.delete_where(
            self.items.dao.table.c.resource_type == "note",
            self.items.dao.table.c.resource_id == note_id,
        )
        self.note_items.dao.delete_where(self.note_items.dao.table.c.note_id == note_id)
        self.notes.delete(note_id)
        self.db.commit()


PRIVATE_ZONE_TABLE_SERVICE_TYPES = {
    "family_group": FamilyGroupService,
    "family_group_member": FamilyGroupMemberService,
    "private_zone_feature": PrivateZoneFeatureService,
    "private_zone_item": PrivateZoneItemService,
    "private_zone_shortcut": PrivateZoneShortcutService,
    "personal_note": PersonalNoteService,
}
