from __future__ import annotations

from typing import Any, Dict, List

from app.providers.base import BaseProvider


class SECProvider(BaseProvider):
    name = "sec"
    enabled = False

    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("SEC EDGAR provider not enabled. Set SEC_USER_AGENT_EMAIL first.")
