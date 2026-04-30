from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)


def setup_scheduler(ingestion_service: IngestionService) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    def mock_job() -> None:
        try:
            result = ingestion_service.run_mock_ingestion()
            logger.info(f"Scheduled mock ingestion: {result['message']}")
        except Exception as exc:
            logger.error(f"Scheduled mock ingestion failed: {exc}")

    scheduler.add_job(
        mock_job,
        "interval",
        minutes=30,
        id="mock_ingestion",
        name="Mock Ingestion",
        replace_existing=True,
    )
    return scheduler
