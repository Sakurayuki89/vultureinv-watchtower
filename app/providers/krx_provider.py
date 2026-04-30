from __future__ import annotations

from typing import Any, Dict, List

from app.providers.base import BaseProvider


class KRXProvider(BaseProvider):
    name = "krx"
    enabled = False

    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("KRX provider not enabled. Configure credentials first.")
