"""Additive endpoints for the server-authored application shell contract."""

from typing import Literal

from fastapi import APIRouter, Query

from app.api.dependencies import Admin, Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.schemas import AppPresentationConfigInput
from app.services.app_shell import AppBootstrapService, AppPresentationService


router = APIRouter(tags=["app-shell"], route_class=OpaqueIdRoute)


@router.get("/learning/app/bootstrap")
def get_app_bootstrap(
    db: Db,
    user: User,
    platform: Literal["android", "ios", "web", "mini"] = "android",
    app_version: str = Query("unknown", min_length=1, max_length=40),
    locale: str = Query("zh-CN", min_length=2, max_length=20),
):
    return AppBootstrapService(db).bootstrap(user, platform, app_version, locale)


@router.get("/learning/app/collections/{collection_code}")
def get_app_collection(
    collection_code: str,
    db: Db,
    user: User,
    platform: Literal["android", "ios", "web", "mini"] = "android",
    q: str = Query("", max_length=200),
    category: str = Query("", max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return AppBootstrapService(db).collection(
        collection_code,
        user,
        platform,
        q=q,
        category=category,
        page=page,
        page_size=page_size,
    )


@router.get("/admin/app-presentation-configs")
def list_app_presentation_configs(db: Db, admin: Admin):
    return AppPresentationService(db).list()


@router.post("/admin/app-presentation-configs", status_code=201)
def create_app_presentation_config(
    payload: AppPresentationConfigInput,
    db: Db,
    admin: Admin,
):
    return AppPresentationService(db).save(payload, admin)


@router.put("/admin/app-presentation-configs/{config_id}")
def update_app_presentation_config(
    config_id: int,
    payload: AppPresentationConfigInput,
    db: Db,
    admin: Admin,
):
    return AppPresentationService(db).save(payload, admin, config_id)


@router.delete("/admin/app-presentation-configs/{config_id}", status_code=204)
def delete_app_presentation_config(config_id: int, db: Db, admin: Admin):
    AppPresentationService(db).delete(config_id)
