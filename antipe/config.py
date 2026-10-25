import os
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Settings:
    database: str = ".local/antipe.sqlite3"
    timezone: str = "America/New_York"
    daily_time: str = "21:00"
    openai_key: str = ""
    model: str = "gpt-4.1"
    meta_token: str = ""
    instagram_id: str = ""
    meta_version: str = "v23.0"
    password: str = ""
    public_base: str = ""
    media_dir: str = ".local/media"

    @classmethod
    def load(cls):
        settings = cls(
            database=os.getenv("ANTIPE_DATABASE", ".local/antipe.sqlite3"),
            timezone=os.getenv("ANTIPE_TIMEZONE", "America/New_York"),
            daily_time=os.getenv("ANTIPE_DAILY_TIME", "21:00"),
            openai_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("ANTIPE_MODEL", "gpt-4.1"),
            meta_token=os.getenv("META_ACCESS_TOKEN", ""),
            instagram_id=os.getenv("INSTAGRAM_ACCOUNT_ID", ""),
            meta_version=os.getenv("META_API_VERSION", "v23.0"),
            password=os.getenv("ANTIPE_PASSWORD", ""),
            public_base=os.getenv("ANTIPE_PUBLIC_URL", "").rstrip('/'),
            media_dir=os.getenv("ANTIPE_MEDIA_DIR", ".local/media"),
        )
        ZoneInfo(settings.timezone)
        hour, minute = map(int, settings.daily_time.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("ANTIPE_DAILY_TIME must be HH:MM in 24-hour time")
        Path(settings.database).parent.mkdir(parents=True, exist_ok=True)
        return settings
