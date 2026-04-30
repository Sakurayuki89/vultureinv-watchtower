from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, HTTPException, Query, Request

router = APIRouter()

_ALLOWED_STATUSES = {"approved", "rejected", "pending"}


@router.get("/review-queue")
def get_review_queue(
    request: Request,
    status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected"),
    limit: int = Query(50, ge=1, le=200),
) -> Dict[str, Any]:
    store = request.app.state.store
    items = store.get_review_queue(status=status, limit=limit)
    return {"items": items, "count": len(items)}


@router.post("/review-queue/{item_id}/status")
def update_queue_item_status(
    item_id: str,
    request: Request,
    body: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    status = body.get("status")
    if status not in _ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"status must be one of: {sorted(_ALLOWED_STATUSES)}",
        )
    store = request.app.state.store
    found = store.update_review_queue_status(item_id, status)
    if not found:
        raise HTTPException(status_code=404, detail="item not found")
    return {"ok": True, "item_id": item_id, "status": status}
