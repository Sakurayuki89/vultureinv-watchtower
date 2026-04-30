from __future__ import annotations

from app.ai.base import BaseAIProvider


class GrokProvider(BaseAIProvider):
    name = "grok"
    enabled = False

    def summarize(self, prompt: str) -> str:
        raise NotImplementedError("Grok provider not enabled. Set GROK_API_KEY and ENABLE_GROK_LIVE=true first.")
