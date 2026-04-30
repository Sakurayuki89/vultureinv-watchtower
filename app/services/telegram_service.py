from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

from app.core.config import Settings
from app.services.ingestion_service import IngestionService
from app.services.snapshot_service import SnapshotService

logger = logging.getLogger(__name__)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.warning("python-telegram-bot not installed — Telegram disabled")


class TelegramService:
    def __init__(
        self,
        settings: Settings,
        snapshot_service: SnapshotService,
        ingestion_service: IngestionService,
    ):
        self.settings = settings
        self.snapshot_service = snapshot_service
        self.ingestion_service = ingestion_service
        self._app: Optional[Any] = None

    async def start(self) -> None:
        if not TELEGRAM_AVAILABLE:
            return
        if not self.settings.telegram_configured:
            logger.info("Telegram not configured (TELEGRAM_BOT_TOKEN empty) — bot disabled")
            return
        try:
            self._app = (
                Application.builder()
                .token(self.settings.telegram_bot_token)
                .build()
            )
            self._app.bot_data["svc"] = self

            self._app.add_handler(CommandHandler("status", self._cmd_status))
            self._app.add_handler(CommandHandler("brief", self._cmd_brief))
            self._app.add_handler(CommandHandler("refresh_mock", self._cmd_refresh_mock))
            self._app.add_handler(CommandHandler("watchlist", self._cmd_watchlist))
            self._app.add_handler(CommandHandler("help", self._cmd_help))

            await self._app.initialize()
            await self._app.start()
            await self._app.updater.start_polling(drop_pending_updates=True)
            logger.info("Telegram bot started")
        except Exception as exc:
            logger.error(f"Telegram start failed: {exc}")
            self._app = None

    async def stop(self) -> None:
        if self._app is None:
            return
        try:
            await self._app.updater.stop()
            await self._app.stop()
            await self._app.shutdown()
            logger.info("Telegram bot stopped")
        except Exception as exc:
            logger.error(f"Telegram stop error: {exc}")

    def _is_allowed(self, chat_id: int) -> bool:
        allowed = self.settings.allowed_chat_ids
        if not allowed:
            return True
        return chat_id in allowed

    async def _cmd_status(self, update: Any, context: Any) -> None:
        if not self._is_allowed(update.effective_chat.id):
            return
        count = self.snapshot_service.get_snapshot_count()
        latest_job = self.snapshot_service.get_latest_job_run()
        job_info = "없음"
        if latest_job:
            job_info = (
                f"{latest_job['job_name']} / {latest_job['status']} "
                f"/ {str(latest_job.get('started_at', ''))[:19]}"
            )
        lines = [
            "📡 Watchtower Status",
            f"환경: {self.settings.watchtower_env}",
            f"스냅샷 수: {count}",
            f"최근 작업: {job_info}",
            f"Telegram: 연결됨",
            f"Live AI: {'ON' if self.settings.enable_live_ai else 'OFF'}",
        ]
        await update.message.reply_text("\n".join(lines))

    async def _cmd_brief(self, update: Any, context: Any) -> None:
        if not self._is_allowed(update.effective_chat.id):
            return
        regime = self.snapshot_service.get_latest("regime")
        flow = self.snapshot_service.get_latest("flow")
        catalysts = self.snapshot_service.get_latest("catalysts")

        if not any([regime, flow, catalysts]):
            await update.message.reply_text(
                "📊 스냅샷 없음\n/refresh_mock 으로 목업 데이터를 생성하세요."
            )
            return

        lines = ["📊 Watchtower Brief"]
        if regime:
            lines.append(
                f"[{regime['freshness_state'].upper()}] {regime['generated_at'][:19]}Z"
            )
            lines.append("\nREGIME:")
            for item in regime["items"]:
                if "regime_label" in item:
                    lines.append(f"  상태: {item['regime_label']}")
                elif "series" in item:
                    sig = item.get("signal", "-")
                    val = item.get("value", "-")
                    lines.append(f"  {item['series']}: {val} ({sig})")

        if flow:
            lines.append("\nFLOW 하이라이트:")
            for item in flow["items"][:4]:
                lines.append(
                    f"  {item.get('symbol')} ({item.get('market')}): "
                    f"{item.get('signal')} [{item.get('score', '-')}]"
                )

        if catalysts:
            lines.append("\nCATALYST:")
            for item in catalysts["items"][:3]:
                lines.append(f"  {item.get('symbol')}: {item.get('title', '-')}")

        if regime and regime.get("warnings"):
            lines.append(f"\n⚠️ {regime['warnings'][0]}")

        await update.message.reply_text("\n".join(lines))

    async def _cmd_refresh_mock(self, update: Any, context: Any) -> None:
        if not self._is_allowed(update.effective_chat.id):
            return
        await update.message.reply_text("⏳ 목업 인제스션 실행 중...")
        try:
            result = await asyncio.to_thread(self.ingestion_service.run_mock_ingestion)
            msg = f"✅ {result['message']}\n생성: {result['generated_at'][:19]}Z"
        except Exception as exc:
            msg = f"❌ 인제스션 실패: {exc}"
        await update.message.reply_text(msg)

    async def _cmd_watchlist(self, update: Any, context: Any) -> None:
        if not self._is_allowed(update.effective_chat.id):
            return
        items = self.snapshot_service.get_watchlist()
        if not items:
            await update.message.reply_text("워치리스트가 비어 있습니다.")
            return
        lines = ["📋 Watchlist"]
        for item in items:
            alert_icon = "🔔" if item["alert_enabled"] else "🔕"
            lines.append(f"  {alert_icon} {item['symbol']} ({item['market']})")
        await update.message.reply_text("\n".join(lines))

    async def _cmd_help(self, update: Any, context: Any) -> None:
        if not self._is_allowed(update.effective_chat.id):
            return
        msg = (
            "🤖 Watchtower 명령어\n\n"
            "/status — 시스템 상태\n"
            "/brief — 최신 브리핑\n"
            "/refresh_mock — 목업 데이터 새로고침\n"
            "/watchlist — 관심 종목 목록\n"
            "/help — 도움말\n\n"
            "⚠️ 이 봇은 투자 조언을 제공하지 않습니다.\n"
            "모든 데이터는 참고용이며 최종 판단은 직접 하십시오."
        )
        await update.message.reply_text(msg)

    async def send_message(self, chat_id: int, text: str) -> None:
        if self._app is None:
            return
        try:
            await self._app.bot.send_message(chat_id=chat_id, text=text)
        except Exception as exc:
            logger.error(f"Failed to send Telegram message to {chat_id}: {exc}")
