from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

_VALID_TYPES = frozenset({"regime", "flow", "catalysts"})


@router.get("/snapshots/{snapshot_type}/latest")
def get_latest_snapshot(snapshot_type: str, request: Request) -> Dict[str, Any]:
    if snapshot_type not in _VALID_TYPES:
        raise HTTPException(status_code=404, detail=f"Unknown snapshot type: {snapshot_type}")
    snapshot_service = request.app.state.snapshot_service
    snapshot = snapshot_service.get_latest(snapshot_type)
    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail=f"No '{snapshot_type}' snapshot found. Run POST /jobs/refresh/mock first.",
        )
    return snapshot
