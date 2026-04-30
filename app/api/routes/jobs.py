from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

_VALID_SOURCES = frozenset({"fred", "opendart", "sec", "krx"})


@router.post("/jobs/refresh/mock")
def refresh_mock(request: Request) -> Dict[str, Any]:
    ingestion_service = request.app.state.ingestion_service
    return ingestion_service.run_mock_ingestion()


@router.post("/jobs/refresh/{source}")
def refresh_source(source: str, request: Request) -> Dict[str, Any]:
    if source not in _VALID_SOURCES:
        raise HTTPException(status_code=404, detail=f"Unknown source: {source}")
    raise HTTPException(
        status_code=501,
        detail=f"Source '{source}' provider not yet implemented. Enable and configure it first.",
    )
