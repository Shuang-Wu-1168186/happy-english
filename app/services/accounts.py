"""Business rules for user accounts and login-audit records."""

import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password
from app.dao.accounts import LoginAuditDAO, UserDAO
from app.dao.membership import MembershipPlanDAO, UserMembershipDAO
from app.services.wechat import VerifiedPhoneNumber


def public_user(row):
    return {key: value for key, value in row.items() if key != "password_hash"}


class LoginAuditService:
    """Service corresponding to the login_audit table."""

    def __init__(self, db):
        self.db = db
        self.dao = LoginAuditDAO(db)

    def record(self, *, username, user_row, login_ip, user_agent, success):
        self.dao.record(
            username=username,
            user_row=user_row,
            login_ip=login_ip,
            user_agent=user_agent,
            success=success,
        )
        self.db.commit()

    def list(self, q, login_ip, outcome, start_date, end_date, page):
        if start_date and end_date and start_date > end_date:
            raise HTTPException(422, "Start date must not be after end date.")
        return self.dao.list_audits(q, login_ip, outcome, start_date, end_date, page)


class UserService:
    """Service corresponding to the user table and account use cases."""

    def __init__(self, db):
        self.db = db
        self.dao = UserDAO(db)
        self.login_audits = LoginAuditService(db)

    def login(self, username, password):
        user = self.dao.by_username(username.strip())
        if not user or not verify_password(password, user["password_hash"]) or user["status"] != "active":
            raise HTTPException(401, "Invalid username or password, or account inactive.")
        return user

    def record_login(self, *, username, user_row, login_ip, user_agent, success):
        self.login_audits.record(
            username=username,
            user_row=user_row,
            login_ip=login_ip,
            user_agent=user_agent,
            success=success,
        )

    def login_with_miniprogram_phone(self, phone: VerifiedPhoneNumber):
        matches = self.dao.by_contact_numbers(phone.lookup_values, phone.normalized_lookup_values)
        if len(matches) > 1:
            raise HTTPException(409, "More than one account uses this phone number. Contact support.")
        if matches:
            user = matches[0]
            if user["status"] != "active":
                raise HTTPException(401, "This account is inactive.")
            return user, False

        for _ in range(5):
            try:
                user = self.dao.create(
                    {
                        "username": f"wx_{secrets.token_hex(10)}",
                        "password_hash": hash_password(secrets.token_urlsafe(48)),
                        "full_name": "微信用户",
                        "contact_number": phone.canonical,
                        "role": "learner",
                        "status": "active",
                    }
                )
                self._grant_default_membership(user["id"])
                self.db.commit()
                return user, True
            except IntegrityError:
                self.db.rollback()
                matches = self.dao.by_contact_numbers(phone.lookup_values, phone.normalized_lookup_values)
                if len(matches) > 1:
                    raise HTTPException(409, "More than one account uses this phone number. Contact support.")
                if matches:
                    user = matches[0]
                    if user["status"] != "active":
                        raise HTTPException(401, "This account is inactive.")
                    return user, False
        raise HTTPException(409, "Unable to create the Mini Program account. Please try again.")

    def create(self, data, *, admin=False):
        values = data.model_dump()
        values["password_hash"] = hash_password(values.pop("password"))
        if not admin:
            values.update(role="learner", status="active")
        result = self.dao.create(values)
        if not admin:
            self._grant_default_membership(result["id"])
        self.db.commit()
        return result

    def _grant_default_membership(self, user_id):
        """Attach the configured default plan when a learner account is created."""
        plan = MembershipPlanDAO(self.db).active_default()
        if not plan:
            return
        starts_at = datetime.now()
        ends_at = (
            starts_at + timedelta(days=plan["duration_days"])
            if plan["duration_days"]
            else None
        )
        UserMembershipDAO(self.db).insert(
            {
                "user_id": user_id,
                "membership_plan_id": plan["id"],
                "status": "active",
                "source": "signup",
                "starts_at": starts_at,
                "ends_at": ends_at,
            }
        )

    def update(self, user_id, data, actor=None):
        if not self.dao.get(user_id):
            raise HTTPException(404, "User not found.")
        values = data.model_dump()
        if actor and actor["id"] == user_id and (values["role"] != "admin" or values["status"] != "active"):
            raise HTTPException(409, "Use another administrator account to disable or demote yourself.")
        result = self.dao.update_user(user_id, values)
        self.db.commit()
        return result

    def change_password(self, user, data):
        if not verify_password(data.old_password, user["password_hash"]):
            raise HTTPException(400, "Current password is incorrect.")
        if data.old_password == data.new_password:
            raise HTTPException(400, "Choose a different password.")
        result = self.dao.update_user(user["id"], {"password_hash": hash_password(data.new_password)})
        self.db.commit()
        return result

    def list_users(self, q, role, status, page, page_size=20):
        return self.dao.list_users(q, role, status, page, page_size)


class AccountService(UserService):
    """Compatibility name for the account API's user service."""
