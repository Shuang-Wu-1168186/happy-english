import hashlib
import hmac
import secrets

import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

COOKIE = "happyenglish_session"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return len(password.encode()) <= 72 and bcrypt.checkpw(password.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False


def password_version(hashed: str, secret: str) -> str:
    return hmac.new(secret.encode(), hashed.encode(), hashlib.sha256).hexdigest()


def serializer(settings):
    return URLSafeTimedSerializer(settings.secret_key, salt="happyenglish-api-session-v1")


def read_session(request) -> dict:
    try:
        return serializer(request.app.state.settings).loads(
            request.cookies.get(COOKIE, ""), max_age=request.app.state.settings.session_seconds
        )
    except (BadSignature, SignatureExpired):
        return {}


def issue_session(response, settings, user=None) -> str:
    token = secrets.token_urlsafe(32)
    data = {"csrf": token}
    if user:
        data.update(uid=user["id"], version=password_version(user["password_hash"], settings.secret_key))
    response.set_cookie(
        COOKIE,
        serializer(settings).dumps(data),
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
        max_age=settings.session_seconds,
    )
    return token
