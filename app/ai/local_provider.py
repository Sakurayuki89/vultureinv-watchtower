from __future__ import annotations

from app.ai.base import BaseAIProvider


class LocalAIProvider(BaseAIProvider):
    name = "local"
    enabled = False

    def summarize(self, prompt: str) -> str:
        raise NotImplementedError("Local/OpenClaw AI provider not enabled. Set OPENCLAW_ENDPOINT first.")
