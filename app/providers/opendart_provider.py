from __future__ import annotations

from typing import Any, Dict, List

from app.providers.base import BaseProvider


class OpenDARTProvider(BaseProvider):
    name = "opendart"
    enabled = False

    def fetch(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("OpenDART provider not enabled. Set OPENDART_API_KEY first.")
