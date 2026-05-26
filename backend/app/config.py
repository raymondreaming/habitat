import os
from dataclasses import dataclass
from typing import List, Optional


DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/habitat"
DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


@dataclass(frozen=True)
class AppConfig:
    database_url: str
    cors_origins: List[str]
    ingest_api_key: Optional[str]


def get_config() -> AppConfig:
    origins = os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS)
    return AppConfig(
        database_url=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL),
        cors_origins=[origin.strip() for origin in origins.split(",") if origin.strip()],
        ingest_api_key=os.getenv("INGEST_API_KEY"),
    )
