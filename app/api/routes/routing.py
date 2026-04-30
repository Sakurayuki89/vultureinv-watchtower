from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()

_VALID_DESTINATIONS = frozenset({"review_queue", "telegram_brief", "vultureinv_snapshot"})


class RoutingRuleIn(BaseModel):
    id: str = ""
    filter_id: str
    enabled: bool = True
    destinations: List[str] = Field(default_factory=lambda: ["review_queue"])
    explain: bool = True


@router.get("/routing")
def get_routing(request: Request) -> Dict[str, Any]:
    store = request.app.state.store
    return {"rules": store.get_routing_rules()}


@router.post("/routing")
def save_routing(body: RoutingRuleIn, request: Request) -> Dict[str, Any]:
    invalid = [d for d in body.destinations if d not in _VALID_DESTINATIONS]
    if invalid:
        return {"ok": False, "error": f"Invalid destinations: {invalid}"}
    store = request.app.state.store
    store.save_routing_rule(body.model_dump())
    return {"ok": True, "rules": store.get_routing_rules()}
