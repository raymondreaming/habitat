from typing import Optional

import psycopg
from psycopg.rows import dict_row

from app.config import get_config


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS auction_results (
      unit_result_id TEXT PRIMARY KEY,
      registered_auction_participant TEXT NOT NULL,
      auction_unit TEXT NOT NULL,
      service_type TEXT NOT NULL,
      auction_product TEXT NOT NULL,
      executed_quantity DOUBLE PRECISION NOT NULL,
      clearing_price DOUBLE PRECISION NOT NULL,
      delivery_start TIMESTAMP NOT NULL,
      delivery_end TIMESTAMP NOT NULL,
      technology_type TEXT,
      post_code TEXT,
      source_resource_id TEXT NOT NULL,
      raw_json JSONB NOT NULL,
      ingested_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ingestion_runs (
      id BIGSERIAL PRIMARY KEY,
      target_date DATE NOT NULL,
      source_resource_id TEXT NOT NULL,
      participant TEXT NOT NULL,
      records_fetched INTEGER NOT NULL DEFAULT 0,
      records_upserted INTEGER NOT NULL DEFAULT 0,
      status TEXT NOT NULL,
      error_message TEXT,
      started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      finished_at TIMESTAMPTZ
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS market_service_totals (
      target_date DATE NOT NULL,
      source_resource_id TEXT NOT NULL,
      service_type TEXT NOT NULL,
      total_records INTEGER NOT NULL,
      total_executed_quantity DOUBLE PRECISION NOT NULL,
      average_clearing_price DOUBLE PRECISION NOT NULL,
      raw_json JSONB NOT NULL,
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      PRIMARY KEY (target_date, source_resource_id, service_type)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_auction_results_delivery_start ON auction_results (delivery_start)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_resource_delivery ON auction_results (source_resource_id, delivery_start)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_resource_service_delivery ON auction_results (source_resource_id, service_type, delivery_start)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_service_type ON auction_results (service_type)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_auction_unit ON auction_results (auction_unit)",
    "CREATE INDEX IF NOT EXISTS idx_market_service_totals_date ON market_service_totals (target_date)",
]


def connect(database_url: Optional[str] = None):
    return psycopg.connect(database_url or get_config().database_url, row_factory=dict_row)


def init_db(database_url: Optional[str] = None) -> None:
    with connect(database_url) as conn:
        with conn.cursor() as cur:
            for statement in SCHEMA_STATEMENTS:
                cur.execute(statement)
