from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict

import httpx
from fastapi import APIRouter, Request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/status")
def status(request: Request) -> Dict[str, Any]:
    settings = request.app.state.settings
    snapshot_service = request.app.state.snapshot_service
    scheduler = request.app.state.scheduler

    scheduler_jobs = []
    scheduler_status = "unknown"
    try:
        for job in scheduler.get_jobs():
            next_run = job.next_run_time.isoformat() if job.next_run_time else None
            scheduler_jobs.append({"id": job.id, "name": job.name, "next_run": next_run})
        scheduler_status = "running" if scheduler.running else "stopped"
    except Exception as exc:
        logger.warning(f"Scheduler status check failed: {exc}")

    vultureinv_reachable = False
    try:
        with httpx.Client(timeout=2.0) as client:
            resp = client.get(f"{settings.vultureinv_api_base_url}/health")
            vultureinv_reachable = resp.status_code == 200
    except Exception:
        pass

    return {
        "service": {
            "status": "ok",
            "env": settings.watchtower_env,
            "version": "0.1.0",
        },
        "scheduler": {
            "status": scheduler_status,
            "jobs": scheduler_jobs,
        },
        "storage": {
            "status": "ok",
            "db_path": settings.db_path,
            "snapshot_count": snapshot_service.get_snapshot_count(),
        },
        "telegram": {
            "configured": settings.telegram_configured,
            "allowed_chat_count": len(settings.allowed_chat_ids),
        },
        "vultureinv": {
            "api_base_url": settings.vultureinv_api_base_url,
            "reachable": vultureinv_reachable,
        },
        "ai": {
            "live_ai_enabled": settings.enable_live_ai,
            "gemini_live_enabled": settings.enable_gemini_live,
            "grok_live_enabled": settings.enable_grok_live,
        },
        "latest_job_run": snapshot_service.get_latest_job_run(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/settings/redacted")
def settings_redacted(request: Request) -> Dict[str, Any]:
    s = request.app.state.settings
    db_url = s.database_url
    db_redacted = db_url.split("///")[0] + "///<redacted>" if "///" in db_url else "<redacted>"
    return {
        "env": s.watchtower_env,
        "database_url_redacted": db_redacted,
        "telegram_configured": s.telegram_configured,
        "allowed_chat_count": len(s.allowed_chat_ids),
        "vultureinv_api_base_url": s.vultureinv_api_base_url,
        "fred_configured": bool(s.fred_api_key),
        "opendart_configured": bool(s.opendart_api_key),
        "sec_user_agent_configured": bool(s.sec_user_agent_email),
        "live_ai_enabled": s.enable_live_ai,
        "openclaw_configured": bool(s.openclaw_endpoint),
        "openclaw_model": s.openclaw_model or None,
        "gemini_configured": bool(s.gemini_api_key),
        "gemini_model": s.gemini_model,
        "gemini_live_enabled": s.enable_gemini_live,
        "grok_configured": bool(s.grok_api_key),
        "grok_model": s.grok_model,
        "grok_live_enabled": s.enable_grok_live,
    }
