from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.repositories.accounts import AccountRepository


class AccountService:
    def __init__(self, db):
        self.db = db
        self.repo = AccountRepository(db)

    def login(self, username, password):
        user = self.repo.by_username(username.strip())
        if not user or not verify_password(password, user["password_hash"]) or user["status"] != "active":
            raise HTTPException(401, "Invalid username or password, or account inactive.")
        return user

    def record_login(self, *, username, user_row, login_ip, user_agent, success):
        self.repo.record_login(
            username=username,
            user_row=user_row,
            login_ip=login_ip,
            user_agent=user_agent,
            success=success,
        )
        self.db.commit()

    def create(self, data, *, admin=False):
        values = data.model_dump()
        values["password_hash"] = hash_password(values.pop("password"))
        if not admin:
            values.update(role="learner", status="active")
        result = self.repo.create(values)
        self.db.commit()
        return result

    def update(self, user_id, data, actor=None):
        if not self.repo.get(user_id):
            raise HTTPException(404, "User not found.")
        values = data.model_dump()
        if actor and actor["id"] == user_id and (values["role"] != "admin" or values["status"] != "active"):
            raise HTTPException(409, "Use another administrator account to disable or demote yourself.")
        result = self.repo.update(user_id, values)
        self.db.commit()
        return result

    def change_password(self, user, data):
        if not verify_password(data.old_password, user["password_hash"]):
            raise HTTPException(400, "Current password is incorrect.")
        if data.old_password == data.new_password:
            raise HTTPException(400, "Choose a different password.")
        result = self.repo.update(user["id"], {"password_hash": hash_password(data.new_password)})
        self.db.commit()
        return result
