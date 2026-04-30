from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Query, Request

router = APIRouter()


@router.get("/review-queue")
def get_review_queue(
    request: Request,
    status: Optional[str] = Query(None, description="Filter by status: pending, approved, rejected"),
    limit: int = Query(50, ge=1, le=200),
) -> Dict[str, Any]:
    store = request.app.state.store
    items = store.get_review_queue(status=status, limit=limit)
    return {"items": items, "count": len(items)}
