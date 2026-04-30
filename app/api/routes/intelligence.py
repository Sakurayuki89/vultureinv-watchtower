from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/intelligence")


@router.post("/run/mock")
def run_mock_intelligence(request: Request) -> Dict[str, Any]:
    svc = request.app.state.intelligence_service
    return svc.run_mock()


@router.get("/status")
def intelligence_status(request: Request) -> Dict[str, Any]:
    svc = request.app.state.intelligence_service
    return svc.get_status()
