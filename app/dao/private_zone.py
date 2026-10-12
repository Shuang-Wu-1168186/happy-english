"""DAOs for family groups and the private learning-zone configuration."""

from sqlalchemy import and_, or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class FamilyGroupDAO(BaseTableDAO):
    table = m.family_group

    def by_invite_code(self, invite_code):
        return (
            self.db.execute(
                select(self.table).where(self.table.c.invite_code == invite_code)
            )
            .mappings()
            .first()
        )

    def list_for_user(self, user_id):
        member = m.family_group_member
        return (
            self.db.execute(
                select(self.table, member.c.role.label("member_role"))
                .join(member, member.c.family_group_id == self.table.c.id)
                .where(
                    member.c.user_id == user_id,
                    member.c.status == "active",
                    self.table.c.status == "active",
                )
                .order_by(self.table.c.created_at, self.table.c.id)
            )
            .mappings()
            .all()
        )


class FamilyGroupMemberDAO(BaseTableDAO):
    table = m.family_group_member

    def find_membership(self, family_group_id, user_id, active_only=False):
        conditions = [
            self.table.c.family_group_id == family_group_id,
            self.table.c.user_id == user_id,
        ]
        if active_only:
            conditions.append(self.table.c.status == "active")
        return self.db.execute(select(self.table).where(*conditions)).mappings().first()

    def list_for_group(self, family_group_id):
        user = m.user
        return (
            self.db.execute(
                select(
                    self.table,
                    user.c.username,
                    user.c.full_name,
                    user.c.email,
                )
                .join(user, user.c.id == self.table.c.user_id)
                .where(self.table.c.family_group_id == family_group_id)
                .order_by(self.table.c.created_at, self.table.c.id)
            )
            .mappings()
            .all()
        )

    def active_group_ids_for_user(self, user_id):
        return self.db.scalars(
            select(self.table.c.family_group_id)
            .where(self.table.c.user_id == user_id, self.table.c.status == "active")
            .order_by(self.table.c.family_group_id)
        ).all()


class PrivateZoneFeatureDAO(BaseTableDAO):
    table = m.private_zone_feature

    def by_code(self, feature_code):
        return self.db.execute(
            select(self.table).where(self.table.c.feature_code == feature_code)
        ).mappings().first()

    def list_features(self, enabled_only=False):
        conditions = []
        if enabled_only:
            conditions.append(self.table.c.is_enabled == 1)
        return self.list_where(*conditions, order_by=[self.table.c.sort_order, self.table.c.id])


class PrivateZoneItemDAO(BaseTableDAO):
    table = m.private_zone_item

    def find_active_duplicate(
        self,
        scope_type,
        owner_user_id,
        family_group_id,
        resource_type,
        resource_id,
    ):
        conditions = [
            self.table.c.scope_type == scope_type,
            self.table.c.resource_type == resource_type,
            self.table.c.resource_id == resource_id,
            self.table.c.status == "active",
        ]
        if scope_type == "personal":
            conditions.append(self.table.c.owner_user_id == owner_user_id)
        else:
            conditions.append(self.table.c.family_group_id == family_group_id)
        return self.db.execute(select(self.table).where(*conditions)).mappings().first()

    def list_for_user(self, user_id, family_group_ids):
        personal = and_(
            self.table.c.scope_type == "personal",
            self.table.c.owner_user_id == user_id,
        )
        family = and_(
            self.table.c.scope_type == "family",
            self.table.c.family_group_id.in_(family_group_ids),
        )
        return self.list_where(
            self.table.c.status == "active",
            or_(personal, family),
            order_by=[self.table.c.sort_order, self.table.c.created_at, self.table.c.id],
        )


class PrivateZoneShortcutDAO(BaseTableDAO):
    table = m.private_zone_shortcut

    def _list_family_shortcuts(self, *conditions):
        family = m.family_group
        return (
            self.db.execute(
                select(
                    self.table,
                    family.c.name.label("family_group_name"),
                )
                .join(family, family.c.id == self.table.c.family_group_id)
                .where(
                    self.table.c.status == "active",
                    self.table.c.scope_type == "family",
                    family.c.status == "active",
                    *conditions,
                )
                .order_by(
                    self.table.c.sort_order,
                    self.table.c.updated_at.desc(),
                    self.table.c.id.desc(),
                )
            )
            .mappings()
            .all()
        )

    def list_for_family_members(self, family_group_ids):
        if not family_group_ids:
            return []
        return self._list_family_shortcuts(
            self.table.c.family_group_id.in_(family_group_ids)
        )

    def list_for_owner_in_families(self, user_id, family_group_ids):
        if not family_group_ids:
            return []
        return self._list_family_shortcuts(
            self.table.c.user_id == user_id,
            self.table.c.family_group_id.in_(family_group_ids),
        )

    def find_active_for_user(self, shortcut_id, user_id):
        return self.find_by_id(
            shortcut_id,
            self.table.c.user_id == user_id,
            self.table.c.status == "active",
            self.table.c.scope_type == "family",
        )


class PersonalNoteDAO(BaseTableDAO):
    table = m.personal_note

    def list_for_user(self, user_id):
        return self.list_where(
            self.table.c.user_id == user_id,
            self.table.c.status == "active",
            order_by=[
                self.table.c.is_pinned.desc(),
                self.table.c.updated_at.desc(),
                self.table.c.id.desc(),
            ],
        )

    def find_active_for_user(self, note_id, user_id):
        return self.find_by_id(
            note_id,
            self.table.c.user_id == user_id,
            self.table.c.status == "active",
        )


PRIVATE_ZONE_TABLE_DAO_TYPES = {
    "family_group": FamilyGroupDAO,
    "family_group_member": FamilyGroupMemberDAO,
    "private_zone_feature": PrivateZoneFeatureDAO,
    "private_zone_item": PrivateZoneItemDAO,
    "private_zone_shortcut": PrivateZoneShortcutDAO,
    "personal_note": PersonalNoteDAO,
}
