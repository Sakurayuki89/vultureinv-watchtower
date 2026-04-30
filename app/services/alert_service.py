from __future__ import annotations

from typing import Any, Dict, List


class AlertService:
    """Alert evaluation — stub for MVP. Extend for real threshold logic."""

    def evaluate(self, snapshot: Dict[str, Any]) -> List[str]:
        return []
