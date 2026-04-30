from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.routes import admin, filters, health, intelligence, jobs, review_queue, routing, snapshots, status
from app.core.config import get_settings
from app.scheduler.jobs import setup_scheduler
from app.services.ingestion_service import IngestionService
from app.services.intelligence_service import IntelligenceService
from app.services.snapshot_service import SnapshotService
from app.services.telegram_service import TelegramService
from app.storage.sqlite_store import SQLiteStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    logger.info(f"Watchtower starting (env={settings.watchtower_env}, port={settings.watchtower_port})")

    store = SQLiteStore(settings.db_path)
    store.init_db()
    logger.info(f"SQLite ready: {settings.db_path}")

    snapshot_service = SnapshotService(store)
    ingestion_service = IngestionService(snapshot_service, store)

    intelligence_service = IntelligenceService(store)

    app.state.settings = settings
    app.state.store = store
    app.state.snapshot_service = snapshot_service
    app.state.ingestion_service = ingestion_service
    app.state.intelligence_service = intelligence_service

    scheduler = setup_scheduler(ingestion_service)
    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("Scheduler started")

    telegram_service = TelegramService(settings, snapshot_service, ingestion_service)
    await telegram_service.start()
    app.state.telegram_service = telegram_service

    yield

    logger.info("Watchtower shutting down")
    await telegram_service.stop()
    scheduler.shutdown(wait=False)
    logger.info("Shutdown complete")


app = FastAPI(
    title="Watchtower",
    description="VultureInv background ingestion and snapshot API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(status.router)
app.include_router(snapshots.router)
app.include_router(jobs.router)
app.include_router(filters.router)
app.include_router(routing.router)
app.include_router(review_queue.router)
app.include_router(intelligence.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn

    cfg = get_settings()
    uvicorn.run("app.main:app", host=cfg.watchtower_host, port=cfg.watchtower_port, reload=False)
