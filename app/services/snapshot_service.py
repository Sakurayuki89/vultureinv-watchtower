from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.storage.sqlite_store import SQLiteStore


class SnapshotService:
    def __init__(self, store: SQLiteStore):
        self.store = store

    def save(self, snapshot: Dict[str, Any]) -> str:
        return self.store.save_snapshot(snapshot)

    def get_latest(self, snapshot_type: str) -> Optional[Dict[str, Any]]:
        return self.store.get_latest_snapshot(snapshot_type)

    def get_watchlist(self) -> List[Dict[str, Any]]:
        return self.store.get_watchlist()

    def get_latest_job_run(self) -> Optional[Dict[str, Any]]:
        return self.store.get_latest_job_run()

    def get_snapshot_count(self) -> int:
        return self.store.get_snapshot_count()
