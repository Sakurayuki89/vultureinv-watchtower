from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class FilterIn(BaseModel):
    id: str = ""
    name: str
    enabled: bool = True
    market_scope: List[str] = Field(default_factory=lambda: ["KR", "US", "KR_ETF", "US_ETF"])
    symbols: List[str] = Field(default_factory=list)
    sectors: List[str] = Field(default_factory=list)
    keywords_include: List[str] = Field(default_factory=list)
    keywords_exclude: List[str] = Field(default_factory=list)
    source_types: List[str] = Field(default_factory=lambda: ["news", "disclosure", "macro", "flow"])
    min_importance: str = "medium"
    freshness_window_minutes: int = 1440
    telegram_enabled: bool = False
    vultureinv_enabled: bool = True
    requires_owner_review: bool = True


@router.get("/filters")
def get_filters(request: Request) -> Dict[str, Any]:
    store = request.app.state.store
    return {"filters": store.get_filters()}


@router.post("/filters")
def save_filter(body: FilterIn, request: Request) -> Dict[str, Any]:
    store = request.app.state.store
    store.save_filter(body.model_dump())
    return {"ok": True, "filters": store.get_filters()}
