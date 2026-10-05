"""DAOs for the user and login_audit tables."""

from datetime import datetime, time, timedelta

from sqlalchemy import func, or_, select

from app import models as m
from app.dao.base import BaseTableDAO


class UserDAO(BaseTableDAO):
    table = m.user
    public_columns = tuple(column for column in table.c if column.name != "password_hash")

    def get(self, user_id):
        return self.find_by_id(user_id)

    def by_username(self, username):
        return self.db.execute(select(self.table).where(self.table.c.username == username)).mappings().first()

    def by_contact_numbers(self, values, normalized_values):
        filters = []
        if values:
            filters.append(self.table.c.contact_number.in_(values))
        if normalized_values:
            normalized_contact = self.table.c.contact_number
            for character in (" ", "-", "+", "(", ")"):
                normalized_contact = func.replace(normalized_contact, character, "")
            filters.append(normalized_contact.in_(normalized_values))
        if not filters:
            return []
        return (
            self.db.execute(select(self.table).where(or_(*filters)).order_by(self.table.c.id))
            .mappings()
            .all()
        )

    def create(self, values):
        return self.get(self.insert(values))

    def update_user(self, user_id, values):
        self.update(user_id, values)
        return self.get(user_id)

    def list_users(self, q, role, status, page, page_size=20):
        filters = []
        if q:
            filters.append(
                or_(
                    *(
                        column.ilike(f"%{q}%")
                        for column in (
                            self.table.c.username,
                            self.table.c.full_name,
                            self.table.c.email,
                            self.table.c.contact_number,
                        )
                    )
                )
            )
        if role:
            filters.append(self.table.c.role == role)
        if status:
            filters.append(self.table.c.status == status)
        total = self.count(*filters)
        rows = (
            self.db.execute(
                select(*self.public_columns)
                .where(*filters)
                .order_by(*self.newest_first_ordering())
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }


class LoginAuditDAO(BaseTableDAO):
    table = m.login_audit

    def record(self, *, username, user_row, login_ip, user_agent, success):
        self.insert(
            {
                "user_id": user_row["id"] if user_row else None,
                "username": username,
                "full_name": user_row["full_name"] if user_row else None,
                "login_ip": login_ip,
                "user_agent": user_agent,
                "success": success,
            }
        )

    def list_audits(self, q, login_ip, outcome, start_date, end_date, page, page_size=20):
        filters = []
        if q:
            filters.append(
                or_(
                    self.table.c.username.ilike(f"%{q}%"),
                    self.table.c.full_name.ilike(f"%{q}%"),
                )
            )
        if login_ip:
            filters.append(self.table.c.login_ip.ilike(f"%{login_ip}%"))
        if outcome:
            filters.append(self.table.c.success.is_(outcome == "success"))
        if start_date:
            filters.append(self.table.c.logged_in_at >= datetime.combine(start_date, time.min))
        if end_date:
            filters.append(
                self.table.c.logged_in_at < datetime.combine(end_date + timedelta(days=1), time.min)
            )
        total = self.count(*filters)
        rows = (
            self.db.execute(
                select(self.table)
                .where(*filters)
                .order_by(self.table.c.logged_in_at.desc(), self.table.c.id.desc())
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
        }


ACCOUNT_TABLE_DAO_TYPES = {
    m.user.name: UserDAO,
    m.login_audit.name: LoginAuditDAO,
}
