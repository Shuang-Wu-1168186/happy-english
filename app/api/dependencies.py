from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import session_scope
from app.core.security import password_version
from app.dao.accounts import UserDAO


def get_db(request: Request):
    yield from session_scope(request.app.state.engine)


Db = Annotated[Session, Depends(get_db)]


def current_user(request: Request, db: Db):
    session = request.state.session
    user = UserDAO(db).get(session.get("uid"))
    if (
        not user
        or user["status"] != "active"
        or session.get("version")
        != password_version(user["password_hash"], request.app.state.settings.secret_key)
    ):
        raise HTTPException(401, "Please log in again.")
    return user


User = Annotated[dict, Depends(current_user)]


def admin_user(user: User):
    if user["role"] != "admin":
        raise HTTPException(403, "Administrator access required.")
    return user


Admin = Annotated[dict, Depends(admin_user)]
