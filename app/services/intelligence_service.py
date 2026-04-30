from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.storage.sqlite_store import SQLiteStore


def _normalize_item(snap_type: str, snapshot_id: str, item: Dict[str, Any]) -> Dict[str, Any]:
    """Extract a flat candidate record from a raw snapshot item."""
    if snap_type == "regime":
        series = item.get("series") or item.get("regime_label", "unknown")
        sig = item.get("signal", "")
        title = f"[macro] {series}" + (f" {sig}" if sig else "")
        content = (item.get("note") or "") + (f" value={item['value']}" if "value" in item else "")
        return {
            "source_type": "macro",
            "snapshot_id": snapshot_id,
            "title": title.strip(),
            "content": content.strip(),
            "market": None,
            "symbol": None,
        }
    elif snap_type == "flow":
        symbol = item.get("symbol", "")
        signal = item.get("signal", "")
        title = f"[flow] {symbol} {signal}".strip()
        content = f"score={item.get('score', '')} note={item.get('note', '')}".strip()
        return {
            "source_type": "flow",
            "snapshot_id": snapshot_id,
            "title": title,
            "content": content,
            "market": item.get("market"),
            "symbol": symbol or None,
        }
    elif snap_type == "catalysts":
        event_type = item.get("event_type", "news")
        source_type = "disclosure" if event_type in ("disclosure", "earnings") else "news"
        title = item.get("title", "")
        content = f"{event_type} source={item.get('source', '')}".strip()
        return {
            "source_type": source_type,
            "snapshot_id": snapshot_id,
            "title": title,
            "content": content,
            "market": item.get("market"),
            "symbol": item.get("symbol") or None,
        }
    return {
        "source_type": "news",
        "snapshot_id": snapshot_id,
        "title": str(item),
        "content": "",
        "market": None,
        "symbol": None,
    }


def _matches_filter(candidate: Dict[str, Any], f: Dict[str, Any]) -> bool:
    """Deterministic filter match — no AI."""
    # source_type must be in filter.source_types
    if candidate["source_type"] not in f.get("source_types", []):
        return False

    # market scope — only checked when item carries a market and filter scopes are set
    market = candidate.get("market")
    market_scope = f.get("market_scope", [])
    if market and market_scope and market not in market_scope:
        return False

    # symbol whitelist — only when filter defines symbols AND item has a symbol
    symbols = f.get("symbols", [])
    symbol = candidate.get("symbol")
    if symbols and symbol and symbol not in symbols:
        return False

    text = f"{candidate['title']} {candidate['content']}".lower()

    # all include keywords must appear (any-match)
    kw_include = f.get("keywords_include", [])
    if kw_include and not any(kw.lower() in text for kw in kw_include):
        return False

    # any exclude keyword blocks the item
    kw_exclude = f.get("keywords_exclude", [])
    if kw_exclude and any(kw.lower() in text for kw in kw_exclude):
        return False

    return True


class IntelligenceService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def run_mock(self) -> Dict[str, Any]:
        warnings: List[str] = []

        # 1. Load latest snapshots
        snap_types = ["regime", "flow", "catalysts"]
        snapshots: Dict[str, Optional[Dict[str, Any]]] = {}
        for snap_type in snap_types:
            snap = self.store.get_latest_snapshot(snap_type)
            snapshots[snap_type] = snap
            if snap is None:
                warnings.append(f"No {snap_type} snapshot found — run /jobs/refresh/mock first")

        # 2. Build flat candidate list
        candidates: List[Dict[str, Any]] = []
        for snap_type, snap in snapshots.items():
            if snap is None:
                continue
            for item in snap.get("items", []):
                candidates.append(_normalize_item(snap_type, snap["snapshot_id"], item))

        if not candidates:
            return {
                "ok": True,
                "created_count": 0,
                "skipped_count": 0,
                "matched_filters": [],
                "warnings": warnings + ["No snapshot items to process"],
            }

        # 3. Load active filters and routing rules indexed by filter_id
        filters = [f for f in self.store.get_filters() if f.get("enabled", True)]
        rules_by_filter: Dict[str, Dict[str, Any]] = {
            r["filter_id"]: r
            for r in self.store.get_routing_rules()
            if r.get("enabled", True)
        }

        if not filters:
            return {
                "ok": True,
                "created_count": 0,
                "skipped_count": len(candidates),
                "matched_filters": [],
                "warnings": warnings + ["No enabled filters configured"],
            }

        # 4. Match, route, create queue items
        created = 0
        skipped = 0
        matched_filter_names: List[str] = []

        for candidate in candidates:
            matched = [f for f in filters if _matches_filter(candidate, f)]
            if not matched:
                skipped += 1
                continue

            for f in matched:
                fname = f.get("name", f["id"])
                if fname not in matched_filter_names:
                    matched_filter_names.append(fname)

                rule = rules_by_filter.get(f["id"])
                should_queue = (
                    (rule is not None and "review_queue" in rule.get("destinations", []))
                    or (rule is None and f.get("requires_owner_review", True))
                )

                if should_queue:
                    queue_item = {
                        "source_type": candidate["source_type"],
                        "snapshot_id": candidate["snapshot_id"],
                        "title": candidate["title"],
                        "content": candidate["content"],
                        "matched_filter_id": f["id"],
                        "routing_rule_id": rule["id"] if rule else "",
                        "status": "pending",
                    }
                    was_created = self.store.add_review_queue_item(queue_item)
                    if was_created:
                        created += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1

        result = {
            "ok": True,
            "created_count": created,
            "skipped_count": skipped,
            "matched_filters": matched_filter_names,
            "warnings": warnings,
        }
        self.store.save_intelligence_run(result)
        return result

    def get_status(self) -> Dict[str, Any]:
        latest_run = self.store.get_latest_intelligence_run()
        counts = self.store.get_review_queue_counts()
        return {
            "latest_run": latest_run,
            "queue_counts": counts,
            "queue_total": sum(counts.values()),
        }
