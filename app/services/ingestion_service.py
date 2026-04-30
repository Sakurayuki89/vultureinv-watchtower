from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.providers.mock_provider import MockProvider
from app.services.snapshot_service import SnapshotService
from app.storage.sqlite_store import SQLiteStore


class IngestionService:
    def __init__(self, snapshot_service: SnapshotService, store: SQLiteStore):
        self.snapshot_service = snapshot_service
        self.store = store
        self.mock_provider = MockProvider()

    def run_mock_ingestion(self) -> Dict[str, Any]:
        job_name = "mock_ingestion"
        run_id = self.store.save_job_run(job_name)
        now = datetime.now(timezone.utc).isoformat()
        snapshot_ids: List[str] = []

        try:
            for snap_type, fetch_fn in [
                ("regime", self.mock_provider.fetch_regime),
                ("flow", self.mock_provider.fetch_flow),
                ("catalysts", self.mock_provider.fetch_catalysts),
            ]:
                snapshot = {
                    "snapshot_id": str(uuid.uuid4()),
                    "snapshot_type": snap_type,
                    "generated_at": now,
                    "source": "mock",
                    "source_fetched_at": now,
                    "freshness_state": "mock",
                    "items": fetch_fn(),
                    "warnings": ["Mock data — no real sources used"],
                }
                sid = self.snapshot_service.save(snapshot)
                snapshot_ids.append(sid)

            self.store.complete_job_run(
                run_id, "success", f"Generated {len(snapshot_ids)} mock snapshots"
            )
            return {
                "ok": True,
                "message": f"Mock ingestion complete — {len(snapshot_ids)} snapshots",
                "snapshot_ids": snapshot_ids,
                "generated_at": now,
            }
        except Exception as exc:
            self.store.complete_job_run(run_id, "failed", str(exc))
            raise
