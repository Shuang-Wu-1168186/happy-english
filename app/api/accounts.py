from datetime import date
from ipaddress import ip_address

from fastapi import APIRouter, HTTPException, Query, Request, Response

from app.api.dependencies import Admin, Db, User, current_user
from app.core.security import issue_session
from app.schemas import (
    AdminCreateInput,
    AdminUpdateInput,
    Credentials,
    MiniProgramLoginInput,
    PasswordInput,
    ProfileInput,
    SignupInput,
)
from app.services.accounts import AccountService, LoginAuditService, public_user
from app.services.wechat import WeChatCredentialError, WeChatServiceError

router = APIRouter(tags=["accounts"])


def login_ip(request: Request):
    """Use the address added by the reverse proxy, falling back to the direct client."""
    candidates = request.headers.get("X-Forwarded-For", "").split(",")
    if request.client:
        candidates.append(request.client.host)
    for candidate in candidates:
        try:
            return str(ip_address(candidate.strip()))
        except ValueError:
            continue
    return None


def login_user_agent(request: Request):
    return request.headers.get("User-Agent", "").strip()[:1000] or None


@router.get("/auth/session")
def session_info(request: Request, response: Response, db: Db):
    user = None
    if request.state.session.get("uid"):
        # Account status and role always come from the database, never an old cookie.
        try:
            user = current_user(request, db)
        except HTTPException as error:
            if error.status_code != 401:
                raise
    csrf = request.state.session.get("csrf")
    if not csrf or (request.state.session.get("uid") and not user):
        csrf = issue_session(
            response,
            request.app.state.settings,
            user,
            auth_method=request.state.session.get("auth_method") if user else None,
        )
    return {
        "user": public_user(user) if user else None,
        "csrf_token": csrf,
        "audio_enabled": request.app.state.settings.audio_enabled,
    }


@router.post("/auth/login")
def login(data: Credentials, request: Request, response: Response, db: Db):
    service = AccountService(db)
    username = data.username.strip()
    metadata = {"login_ip": login_ip(request), "user_agent": login_user_agent(request)}
    try:
        user = service.login(username, data.password)
    except HTTPException:
        service.record_login(username=username, user_row=None, success=False, **metadata)
        raise
    service.record_login(username=username, user_row=user, success=True, **metadata)
    csrf = issue_session(response, request.app.state.settings, user)
    return {"user": public_user(user), "csrf_token": csrf}


@router.post("/auth/miniprogram/login")
def miniprogram_login(data: MiniProgramLoginInput, request: Request, response: Response, db: Db):
    service = AccountService(db)
    metadata = {"login_ip": login_ip(request), "user_agent": login_user_agent(request)}
    try:
        wechat = request.app.state.wechat_miniprogram
        # Exchange wx.login's code as well as the phone authorization code. Neither phone
        # numbers nor account identifiers are accepted from the Mini Program directly.
        wechat.exchange_login_code(data.login_code)
        phone = wechat.get_phone_number(data.phone_code)
        user, created = service.login_with_miniprogram_phone(phone)
    except WeChatCredentialError as error:
        service.record_login(username="wechat_miniprogram", user_row=None, success=False, **metadata)
        raise HTTPException(401, "微信登录凭证已失效，请重新授权手机号。") from error
    except WeChatServiceError as error:
        service.record_login(username="wechat_miniprogram", user_row=None, success=False, **metadata)
        raise HTTPException(503, "微信登录服务暂时不可用，请稍后重试。") from error
    except HTTPException:
        service.record_login(username="wechat_miniprogram", user_row=None, success=False, **metadata)
        raise
    service.record_login(username=user["username"], user_row=user, success=True, **metadata)
    csrf = issue_session(
        response,
        request.app.state.settings,
        user,
        auth_method="wechat_miniprogram",
    )
    return {"user": public_user(user), "csrf_token": csrf, "created": created}


@router.post("/auth/logout")
def logout(request: Request, response: Response):
    csrf = issue_session(response, request.app.state.settings)
    return {"user": None, "csrf_token": csrf}


@router.post("/auth/signup", status_code=201)
def signup(data: SignupInput, db: Db):
    return public_user(AccountService(db).create(data))


@router.put("/profile")
def profile(data: ProfileInput, db: Db, user: User):
    return public_user(AccountService(db).update(user["id"], data))


@router.post("/profile/password")
def password(data: PasswordInput, request: Request, response: Response, db: Db, user: User):
    updated = AccountService(db).change_password(user, data)
    csrf = issue_session(response, request.app.state.settings, updated)
    return {"csrf_token": csrf}


@router.get("/admin/users")
def users(
    db: Db,
    admin: Admin,
    q: str = Query("", max_length=200),
    role: str = "",
    status: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return AccountService(db).list_users(q, role, status, page, page_size)


@router.get("/admin/login-audits")
def login_audits(
    db: Db,
    admin: Admin,
    q: str = Query("", max_length=200),
    login_ip: str = Query("", max_length=45),
    outcome: str = Query("", pattern="^(|success|failed)$"),
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = Query(1, ge=1),
):
    return LoginAuditService(db).list(q, login_ip, outcome, start_date, end_date, page)


@router.post("/admin/users", status_code=201)
def create_user(data: AdminCreateInput, db: Db, admin: Admin):
    return public_user(AccountService(db).create(data, admin=True))


@router.put("/admin/users/{user_id}")
def update_user(user_id: int, data: AdminUpdateInput, db: Db, admin: Admin):
    return public_user(AccountService(db).update(user_id, data, actor=admin))
