from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseProvider(ABC):
    name: str = "base"
    enabled: bool = False

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch raw items from source. Returns list of raw item dicts."""
        ...

    def is_available(self) -> bool:
        return self.enabled
