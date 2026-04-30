from __future__ import annotations

from typing import Any, Dict, List

from app.providers.base import BaseProvider


class FREDProvider(BaseProvider):
    name = "fred"
    enabled = False

    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("FRED provider not enabled. Set FRED_API_KEY first.")
