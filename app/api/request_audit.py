"""Administrator access to request activity parsed from application logs."""

from datetime import date

from fastapi import APIRouter, Query, Request

from app.api.dependencies import Admin
from app.api.opaque_ids import OpaqueIdRoute
from app.services.request_audit import RequestAuditService


router = APIRouter(tags=["request-audit"], route_class=OpaqueIdRoute)


@router.get("/admin/request-audits")
def list_request_audits(
    request: Request,
    admin: Admin,
    username: str = Query("", max_length=100),
    path: str = Query("", max_length=300),
    method: str = Query("", pattern=r"^(|GET|POST|PUT|PATCH|DELETE|OPTIONS)$"),
    status: int | None = Query(None, ge=100, le=599),
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
):
    return RequestAuditService(request.app.state.settings).list(
        username=username,
        path=path,
        method=method,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )


@router.get("/admin/request-audits/report")
def request_audit_report(
    request: Request,
    admin: Admin,
    username: str = Query("", max_length=100),
    path: str = Query("", max_length=300),
    method: str = Query("", pattern=r"^(|GET|POST|PUT|PATCH|DELETE|OPTIONS)$"),
    status: int | None = Query(None, ge=100, le=599),
    start_date: date | None = None,
    end_date: date | None = None,
):
    return RequestAuditService(request.app.state.settings).report(
        username=username,
        path=path,
        method=method,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/admin/request-audits/user-report")
def request_audit_user_report(
    request: Request,
    admin: Admin,
    username: str = Query("", max_length=100),
    path: str = Query("", max_length=300),
    method: str = Query("", pattern=r"^(|GET|POST|PUT|PATCH|DELETE|OPTIONS)$"),
    status: int | None = Query(None, ge=100, le=599),
    start_date: date | None = None,
    end_date: date | None = None,
):
    report = RequestAuditService(request.app.state.settings).report(
        username=username,
        path=path,
        method=method,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    return {
        "overview": report["overview"],
        "users": report["users"],
        "daily": report["daily"],
    }


@router.get("/admin/request-audits/latency-report")
def request_audit_latency_report(
    request: Request,
    admin: Admin,
    username: str = Query("", max_length=100),
    path: str = Query("", max_length=300),
    method: str = Query("", pattern=r"^(|GET|POST|PUT|PATCH|DELETE|OPTIONS)$"),
    status: int | None = Query(None, ge=100, le=599),
    start_date: date | None = None,
    end_date: date | None = None,
):
    report = RequestAuditService(request.app.state.settings).report(
        username=username,
        path=path,
        method=method,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    return {
        "overview": report["overview"],
        "endpoints": report["endpoints"],
        "daily": report["daily"],
    }
