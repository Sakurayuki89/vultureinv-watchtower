from __future__ import annotations

from app.ai.base import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    name = "gemini"
    enabled = False

    def summarize(self, prompt: str) -> str:
        raise NotImplementedError("Gemini provider not enabled. Set GEMINI_API_KEY and ENABLE_GEMINI_LIVE=true first.")
