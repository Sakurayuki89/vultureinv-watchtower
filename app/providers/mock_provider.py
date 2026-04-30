from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from app.providers.base import BaseProvider


class MockProvider(BaseProvider):
    name = "mock"
    enabled = True

    def fetch(self) -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        return [{"provider": "mock", "fetched_at": now, "data_type": "mock_signal"}]

    def fetch_regime(self) -> List[Dict[str, Any]]:
        return [
            {"series": "VIX", "value": 18.5, "signal": "neutral", "note": "mock"},
            {"series": "US10Y", "value": 4.35, "signal": "cautious", "note": "mock"},
            {"series": "DXY", "value": 103.2, "signal": "neutral", "note": "mock"},
            {"series": "SPY", "value": 518.5, "change_pct": 0.3, "note": "mock"},
            {"series": "KOSPI", "value": 2620.5, "change_pct": -0.2, "note": "mock"},
            {"series": "KOSDAQ", "value": 845.3, "change_pct": 0.1, "note": "mock"},
            {"regime_label": "NEUTRAL", "note": "mock"},
        ]

    def fetch_flow(self) -> List[Dict[str, Any]]:
        return [
            {"symbol": "005930", "market": "KR", "signal": "accumulation", "score": 0.72, "note": "mock"},
            {"symbol": "035720", "market": "KR", "signal": "neutral", "score": 0.45, "note": "mock"},
            {"symbol": "000660", "market": "KR", "signal": "distribution", "score": 0.28, "note": "mock"},
            {"symbol": "AAPL", "market": "US", "signal": "distribution", "score": 0.35, "note": "mock"},
            {"symbol": "MSFT", "market": "US", "signal": "accumulation", "score": 0.61, "note": "mock"},
        ]

    def fetch_catalysts(self) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": "005930",
                "market": "KR",
                "event_type": "disclosure",
                "title": "[Mock] 분기 실적 가이던스 업데이트",
                "source": "mock",
            },
            {
                "symbol": "000660",
                "market": "KR",
                "event_type": "disclosure",
                "title": "[Mock] 대규모 설비투자 공시",
                "source": "mock",
            },
            {
                "symbol": "AAPL",
                "market": "US",
                "event_type": "earnings",
                "title": "[Mock] Earnings beat +12% YoY",
                "source": "mock",
            },
        ]
