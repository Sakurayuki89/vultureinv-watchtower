from __future__ import annotations

from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    watchtower_env: str = "local"
    watchtower_host: str = "127.0.0.1"
    watchtower_port: int = 8010

    database_url: str = "sqlite:///./data/watchtower.sqlite3"

    telegram_bot_token: str = ""
    telegram_allowed_chat_ids: str = ""

    vultureinv_api_base_url: str = "http://127.0.0.1:8001"
    watchtower_api_token: str = ""

    fred_api_key: str = ""
    opendart_api_key: str = ""
    sec_user_agent_company: str = "VultureInv"
    sec_user_agent_email: str = ""

    enable_live_ai: bool = False
    openclaw_endpoint: str = ""
    openclaw_model: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash-lite"
    enable_gemini_live: bool = False
    grok_api_key: str = ""
    grok_model: str = "grok-4.20"
    enable_grok_live: bool = False

    @property
    def allowed_chat_ids(self) -> List[int]:
        raw = self.telegram_allowed_chat_ids.strip()
        if not raw:
            return []
        result = []
        for part in raw.split(","):
            part = part.strip()
            if part:
                try:
                    result.append(int(part))
                except ValueError:
                    pass
        return result

    @property
    def telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token.strip())

    @property
    def db_path(self) -> str:
        url = self.database_url
        if url.startswith("sqlite:///"):
            return url[len("sqlite:///"):]
        return url


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
