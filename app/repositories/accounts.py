from datetime import datetime, time, timedelta

from sqlalchemy import func, or_, select

from app.models import login_audit, user

PUBLIC_COLUMNS = tuple(c for c in user.c if c.name != "password_hash")


class AccountRepository:
    def __init__(self, db):
        self.db = db

    def get(self, user_id):
        return self.db.execute(select(user).where(user.c.id == user_id)).mappings().first()

    def by_username(self, username):
        return self.db.execute(select(user).where(user.c.username == username)).mappings().first()

    def create(self, values):
        result = self.db.execute(user.insert().values(**values))
        return self.get(result.inserted_primary_key[0])

    def update(self, user_id, values):
        self.db.execute(user.update().where(user.c.id == user_id).values(**values, updated_at=func.now()))
        return self.get(user_id)

    def list(self, q, role, status, page):
        filters = []
        if q:
            filters.append(
                or_(*(c.ilike(f"%{q}%") for c in (user.c.username, user.c.full_name, user.c.email)))
            )
        if role:
            filters.append(user.c.role == role)
        if status:
            filters.append(user.c.status == status)
        total = self.db.scalar(select(func.count()).select_from(user).where(*filters))
        rows = (
            self.db.execute(
                select(*PUBLIC_COLUMNS)
                .where(*filters)
                .order_by(user.c.id.desc())
                .limit(20)
                .offset((page - 1) * 20)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "page": page,
            "page_size": 20,
            "total": total,
            "total_pages": max(1, (total + 19) // 20),
        }

    def record_login(self, *, username, user_row, login_ip, user_agent, success):
        self.db.execute(
            login_audit.insert().values(
                user_id=user_row["id"] if user_row else None,
                username=username,
                full_name=user_row["full_name"] if user_row else None,
                login_ip=login_ip,
                user_agent=user_agent,
                success=success,
            )
        )

    def list_login_audits(self, q, login_ip, outcome, start_date, end_date, page):
        filters = []
        if q:
            filters.append(
                or_(
                    login_audit.c.username.ilike(f"%{q}%"),
                    login_audit.c.full_name.ilike(f"%{q}%"),
                )
            )
        if login_ip:
            filters.append(login_audit.c.login_ip.ilike(f"%{login_ip}%"))
        if outcome:
            filters.append(login_audit.c.success.is_(outcome == "success"))
        if start_date:
            filters.append(login_audit.c.logged_in_at >= datetime.combine(start_date, time.min))
        if end_date:
            filters.append(
                login_audit.c.logged_in_at < datetime.combine(end_date + timedelta(days=1), time.min)
            )
        total = self.db.scalar(select(func.count()).select_from(login_audit).where(*filters))
        rows = (
            self.db.execute(
                select(login_audit)
                .where(*filters)
                .order_by(login_audit.c.logged_in_at.desc(), login_audit.c.id.desc())
                .limit(20)
                .offset((page - 1) * 20)
            )
            .mappings()
            .all()
        )
        return {
            "items": rows,
            "page": page,
            "page_size": 20,
            "total": total,
            "total_pages": max(1, (total + 19) // 20),
        }


def public_user(row):
    return {key: value for key, value in row.items() if key != "password_hash"}
