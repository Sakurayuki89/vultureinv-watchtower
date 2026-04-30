from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "watchtower",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
