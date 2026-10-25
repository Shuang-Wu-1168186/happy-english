"""Analytics ingestion and event-dictionary endpoints."""

from fastapi import APIRouter

from app.api.dependencies import Admin, Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.schemas import AnalyticsEventBatchInput, AnalyticsEventDefinitionInput
from app.services.analytics import AnalyticsService


router = APIRouter(tags=["analytics"], route_class=OpaqueIdRoute)
admin_router = APIRouter(tags=["analytics"], route_class=OpaqueIdRoute)


@router.get("/analytics/policy")
def get_analytics_policy(db: Db, user: User):
    return AnalyticsService(db).policy()


@router.post("/analytics/events:batch", status_code=202)
def record_analytics_events(payload: AnalyticsEventBatchInput, db: Db, user: User):
    return AnalyticsService(db).record_batch(payload, user)


@admin_router.get("/admin/analytics/event-definitions")
def list_analytics_event_definitions(db: Db, admin: Admin):
    return AnalyticsService(db).list_definitions()


@admin_router.post("/admin/analytics/event-definitions", status_code=201)
def create_analytics_event_definition(
    payload: AnalyticsEventDefinitionInput,
    db: Db,
    admin: Admin,
):
    return AnalyticsService(db).save_definition(payload, admin)


@admin_router.put("/admin/analytics/event-definitions/{event_name}")
def update_analytics_event_definition(
    event_name: str,
    payload: AnalyticsEventDefinitionInput,
    db: Db,
    admin: Admin,
):
    return AnalyticsService(db).save_definition(payload, admin, event_name)
