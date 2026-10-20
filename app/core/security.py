import hashlib
import hmac
import secrets

import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.opaque_ids import OpaqueIdError, codec_from_settings

COOKIE = "happyenglish_session"
SESSION_HEADER = "X-Happy-English-Session"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return len(password.encode()) <= 72 and bcrypt.checkpw(password.encode(), hashed.encode())
    except (ValueError, TypeError):
        return False


def authentication_version(user, secret: str) -> str:
    """Return the server-checked version for a signed client session.

    Password changes always invalidate sessions. The independent per-user
    session version additionally lets logout revoke copied cookies and mobile
    session headers immediately.
    """

    session_version = str(user.get("session_version") or "")
    material = f"{user['password_hash']}:{session_version}".encode()
    return hmac.new(secret.encode(), material, hashlib.sha256).hexdigest()


def serializer(settings):
    return URLSafeTimedSerializer(settings.secret_key, salt="happyenglish-api-session-v1")


def read_session(request) -> dict:
    for value in (request.headers.get(SESSION_HEADER, ""), request.cookies.get(COOKIE, "")):
        try:
            if value:
                data = serializer(request.app.state.settings).loads(
                    value, max_age=request.app.state.settings.session_seconds
                )
                if data.get("uid"):
                    data["uid"] = codec_from_settings(request.app.state.settings).decode(data["uid"])
                return data
        except (BadSignature, SignatureExpired, OpaqueIdError):
            continue
    return {}


def issue_session(
    response,
    settings,
    user=None,
    *,
    auth_method: str | None = None,
    csrf_token: str | None = None,
) -> str:
    token = csrf_token or secrets.token_urlsafe(32)
    data = {"csrf": token}
    if user:
        data.update(
            uid=codec_from_settings(settings).encode(user["id"]),
            version=authentication_version(user, settings.secret_key),
        )
        if auth_method:
            data["auth_method"] = auth_method
    session_value = serializer(settings).dumps(data)
    response.set_cookie(
        COOKIE,
        session_value,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
        max_age=settings.session_seconds,
    )
    response.headers[SESSION_HEADER] = session_value
    return token
