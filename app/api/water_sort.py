"""Authenticated mobile game API. All public IDs are UUIDs or stable curriculum codes."""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.api.dependencies import Db, User
from app.api.opaque_ids import OpaqueIdRoute
from app.services.water_sort import WaterSortProgressService, WaterSortService
from app.services.water_sort_catalog import WaterSortCatalog, public_word

router = APIRouter(prefix="/game/v1/water-sort", tags=["water-sort"], route_class=OpaqueIdRoute)


class StartInput(BaseModel):
    level_number: int = Field(ge=1, le=810)
    request_id: UUID
    campaign_version: Literal[7] = 7


class ActionInput(BaseModel):
    request_id: UUID
    revision: int = Field(ge=0)
    action: Literal["pour", "undo", "restart", "acknowledge", "complete", "challenge", "answer"]
    source: int = Field(default=-1, ge=-1, le=24)
    target: int = Field(default=-1, ge=-1, le=24)
    amount: int = Field(default=0, ge=0, le=5)
    bottle: int = Field(default=-1, ge=-1, le=24)
    challenge_id: str = Field(default="", max_length=36)
    question_id: str = Field(default="", max_length=36)
    option_id: str = Field(default="", max_length=32)


@router.get("/progress")
def progress(db: Db, user: User):
    return {"campaign_version": 7, "total_levels": 810,
            **WaterSortProgressService(db).get(user)}


@router.get("/vocabulary")
def vocabulary(db: Db, user: User, book: int = Query(ge=1, le=12), offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    catalog = WaterSortCatalog(db, user)
    words = [w for w in catalog.words if w["book"] == book and catalog.allowed(w)]
    return {"book": book, "accessible_words": len(words),
            "total_words": sum(w["book"] == book for w in catalog.words),
            "items": [public_word(w) for w in words[offset:offset + limit]]}


@router.post("/levels:next")
def start(data: StartInput, db: Db, user: User):
    return WaterSortService(db).start(user, data.level_number, str(data.request_id), data.campaign_version)


@router.post("/attempts/{attempt_id}/actions")
def action(attempt_id: UUID, data: ActionInput, db: Db, user: User):
    return WaterSortService(db).action(user, str(attempt_id), data)
