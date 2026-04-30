from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    name: str = "base"
    enabled: bool = False

    @abstractmethod
    def summarize(self, prompt: str) -> str:
        ...

    def is_available(self) -> bool:
        return self.enabled
