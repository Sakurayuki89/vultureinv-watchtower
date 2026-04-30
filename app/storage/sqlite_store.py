from __future__ import annotations

import contextlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional


class SQLiteStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextlib.contextmanager
    def _connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        with self._connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS filters (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    config_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS routing_rules (
                    id TEXT PRIMARY KEY,
                    filter_id TEXT NOT NULL,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    destinations_json TEXT NOT NULL DEFAULT '["review_queue"]',
                    explain INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS review_queue (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    source_type TEXT NOT NULL DEFAULT 'news',
                    snapshot_id TEXT NOT NULL DEFAULT '',
                    title TEXT NOT NULL DEFAULT '',
                    content TEXT NOT NULL DEFAULT '',
                    matched_filter_id TEXT NOT NULL DEFAULT '',
                    routing_rule_id TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pending',
                    reviewed_at TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_review_queue_status
                ON review_queue(status, created_at DESC)
            """)
            conn.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_review_queue_dedup
                ON review_queue(snapshot_id, title, matched_filter_id)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS intelligence_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ran_at TEXT NOT NULL,
                    created_count INTEGER NOT NULL DEFAULT 0,
                    skipped_count INTEGER NOT NULL DEFAULT 0,
                    matched_filters_json TEXT NOT NULL DEFAULT '[]',
                    warnings_json TEXT NOT NULL DEFAULT '[]'
                )
            """)
            cursor_f = conn.execute("SELECT COUNT(*) FROM filters")
            if cursor_f.fetchone()[0] == 0:
                self._seed_filters(conn)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id TEXT UNIQUE NOT NULL,
                    snapshot_type TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    source_fetched_at TEXT NOT NULL,
                    freshness_state TEXT NOT NULL,
                    items_json TEXT NOT NULL DEFAULT '[]',
                    warnings_json TEXT NOT NULL DEFAULT '[]'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_snapshots_type_time
                ON snapshots(snapshot_type, generated_at DESC)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_name TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT NOT NULL DEFAULT 'running',
                    message TEXT DEFAULT ''
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS watchlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    market TEXT NOT NULL DEFAULT 'KR',
                    alert_enabled INTEGER NOT NULL DEFAULT 1,
                    added_at TEXT NOT NULL,
                    UNIQUE(symbol, market)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alert_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    symbol TEXT,
                    message TEXT NOT NULL,
                    sent_at TEXT,
                    snapshot_id TEXT
                )
            """)
            cursor = conn.execute("SELECT COUNT(*) FROM watchlist")
            if cursor.fetchone()[0] == 0:
                self._seed_watchlist(conn)
            conn.commit()

    def _seed_filters(self, conn: sqlite3.Connection) -> None:
        now = datetime.now(timezone.utc).isoformat()
        default_filter = {
            "id": "default",
            "name": "Default",
            "enabled": True,
            "market_scope": ["KR", "US", "KR_ETF", "US_ETF"],
            "symbols": [],
            "sectors": [],
            "keywords_include": [],
            "keywords_exclude": [],
            "source_types": ["news", "disclosure", "macro", "flow"],
            "min_importance": "medium",
            "freshness_window_minutes": 1440,
            "telegram_enabled": False,
            "vultureinv_enabled": True,
            "requires_owner_review": True,
        }
        conn.execute(
            "INSERT OR IGNORE INTO filters (id, name, enabled, config_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("default", "Default", 1, json.dumps(default_filter), now, now),
        )

    def _seed_watchlist(self, conn: sqlite3.Connection) -> None:
        now = datetime.now(timezone.utc).isoformat()
        defaults = [
            ("005930", "KR"),
            ("035720", "KR"),
            ("000660", "KR"),
            ("AAPL", "US"),
            ("MSFT", "US"),
            ("SPY", "US"),
        ]
        for symbol, market in defaults:
            conn.execute(
                "INSERT OR IGNORE INTO watchlist (symbol, market, alert_enabled, added_at) VALUES (?, ?, 1, ?)",
                (symbol, market, now),
            )

    def save_snapshot(self, snapshot: Dict[str, Any]) -> str:
        snapshot_id = snapshot.get("snapshot_id") or str(uuid.uuid4())
        with self._connection() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO snapshots
                   (snapshot_id, snapshot_type, generated_at, source,
                    source_fetched_at, freshness_state, items_json, warnings_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    snapshot_id,
                    snapshot["snapshot_type"],
                    snapshot["generated_at"],
                    snapshot["source"],
                    snapshot["source_fetched_at"],
                    snapshot["freshness_state"],
                    json.dumps(snapshot.get("items", [])),
                    json.dumps(snapshot.get("warnings", [])),
                ),
            )
            conn.commit()
        return snapshot_id

    def get_latest_snapshot(self, snapshot_type: str) -> Optional[Dict[str, Any]]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM snapshots WHERE snapshot_type = ? ORDER BY generated_at DESC LIMIT 1",
                (snapshot_type,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_snapshot(row)

    def _row_to_snapshot(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "snapshot_id": row["snapshot_id"],
            "snapshot_type": row["snapshot_type"],
            "generated_at": row["generated_at"],
            "source": row["source"],
            "source_fetched_at": row["source_fetched_at"],
            "freshness_state": row["freshness_state"],
            "items": json.loads(row["items_json"]),
            "warnings": json.loads(row["warnings_json"]),
        }

    def save_job_run(self, job_name: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO job_runs (job_name, started_at, status) VALUES (?, ?, 'running')",
                (job_name, now),
            )
            conn.commit()
            return cursor.lastrowid

    def complete_job_run(self, run_id: int, status: str, message: str = "") -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connection() as conn:
            conn.execute(
                "UPDATE job_runs SET finished_at = ?, status = ?, message = ? WHERE id = ?",
                (now, status, message, run_id),
            )
            conn.commit()

    def get_latest_job_run(self, job_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        with self._connection() as conn:
            if job_name:
                row = conn.execute(
                    "SELECT * FROM job_runs WHERE job_name = ? ORDER BY started_at DESC LIMIT 1",
                    (job_name,),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT * FROM job_runs ORDER BY started_at DESC LIMIT 1"
                ).fetchone()
        if row is None:
            return None
        return dict(row)

    def get_watchlist(self) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT * FROM watchlist ORDER BY market, symbol"
            ).fetchall()
        return [dict(row) for row in rows]

    def get_snapshot_count(self) -> int:
        with self._connection() as conn:
            row = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()
        return row[0] if row else 0

    # --- Filters ---

    def get_filters(self) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            rows = conn.execute("SELECT * FROM filters ORDER BY created_at").fetchall()
        result = []
        for row in rows:
            d = json.loads(row["config_json"])
            d["id"] = row["id"]
            d["name"] = row["name"]
            d["enabled"] = bool(row["enabled"])
            d["created_at"] = row["created_at"]
            d["updated_at"] = row["updated_at"]
            result.append(d)
        return result

    def save_filter(self, f: Dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        fid = f.get("id") or str(uuid.uuid4())
        name = f.get("name", "Unnamed")
        enabled = 1 if f.get("enabled", True) else 0
        config = {k: v for k, v in f.items() if k not in ("id", "name", "enabled", "created_at", "updated_at")}
        with self._connection() as conn:
            existing = conn.execute("SELECT created_at FROM filters WHERE id = ?", (fid,)).fetchone()
            created_at = existing["created_at"] if existing else now
            conn.execute(
                "INSERT OR REPLACE INTO filters (id, name, enabled, config_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (fid, name, enabled, json.dumps(config), created_at, now),
            )
            conn.commit()

    # --- Routing rules ---

    def get_routing_rules(self) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            rows = conn.execute("SELECT * FROM routing_rules ORDER BY created_at").fetchall()
        return [
            {
                "id": row["id"],
                "filter_id": row["filter_id"],
                "enabled": bool(row["enabled"]),
                "destinations": json.loads(row["destinations_json"]),
                "explain": bool(row["explain"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def save_routing_rule(self, rule: Dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        rid = rule.get("id") or str(uuid.uuid4())
        enabled = 1 if rule.get("enabled", True) else 0
        explain = 1 if rule.get("explain", True) else 0
        with self._connection() as conn:
            existing = conn.execute("SELECT created_at FROM routing_rules WHERE id = ?", (rid,)).fetchone()
            created_at = existing["created_at"] if existing else now
            conn.execute(
                "INSERT OR REPLACE INTO routing_rules (id, filter_id, enabled, destinations_json, explain, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (rid, rule.get("filter_id", ""), enabled, json.dumps(rule.get("destinations", ["review_queue"])), explain, created_at, now),
            )
            conn.commit()

    # --- Review queue ---

    def get_review_queue(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM review_queue WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                    (status, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM review_queue ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        return [dict(row) for row in rows]

    def add_review_queue_item(self, item: Dict[str, Any]) -> bool:
        """Insert a review queue item. Returns True if created, False if duplicate."""
        now = datetime.now(timezone.utc).isoformat()
        item_id = item.get("id") or str(uuid.uuid4())
        with self._connection() as conn:
            cursor = conn.execute(
                """INSERT OR IGNORE INTO review_queue
                   (id, created_at, source_type, snapshot_id, title, content,
                    matched_filter_id, routing_rule_id, status, reviewed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    item_id,
                    item.get("created_at", now),
                    item.get("source_type", "news"),
                    item.get("snapshot_id", ""),
                    item.get("title", ""),
                    item.get("content", ""),
                    item.get("matched_filter_id", ""),
                    item.get("routing_rule_id", ""),
                    item.get("status", "pending"),
                    item.get("reviewed_at"),
                ),
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_review_queue_counts(self) -> Dict[str, int]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) AS cnt FROM review_queue GROUP BY status"
            ).fetchall()
        return {row["status"]: row["cnt"] for row in rows}

    # --- Intelligence runs ---

    def save_intelligence_run(self, result: Dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO intelligence_runs
                   (ran_at, created_count, skipped_count, matched_filters_json, warnings_json)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    now,
                    result.get("created_count", 0),
                    result.get("skipped_count", 0),
                    json.dumps(result.get("matched_filters", [])),
                    json.dumps(result.get("warnings", [])),
                ),
            )
            conn.commit()

    def get_latest_intelligence_run(self) -> Optional[Dict[str, Any]]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM intelligence_runs ORDER BY ran_at DESC LIMIT 1"
            ).fetchone()
        if row is None:
            return None
        return {
            "ran_at": row["ran_at"],
            "created_count": row["created_count"],
            "skipped_count": row["skipped_count"],
            "matched_filters": json.loads(row["matched_filters_json"]),
            "warnings": json.loads(row["warnings_json"]),
        }
