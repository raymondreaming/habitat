from datetime import date, datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.config import get_config
from app.neso import PARTICIPANT, RESOURCE_ID


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
    "CREATE INDEX IF NOT EXISTS idx_auction_results_delivery_start ON auction_results (delivery_start)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_service_type ON auction_results (service_type)",
    "CREATE INDEX IF NOT EXISTS idx_auction_results_auction_unit ON auction_results (auction_unit)",
]


def connect(database_url: str = None):
    return psycopg.connect(database_url or get_config().database_url, row_factory=dict_row)


def init_db(database_url: str = None) -> None:
    with connect(database_url) as conn:
        with conn.cursor() as cur:
            for statement in SCHEMA_STATEMENTS:
                cur.execute(statement)


def create_ingestion_run(conn, target_date: date) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingestion_runs (target_date, source_resource_id, participant, status)
            VALUES (%s, %s, %s, 'running')
            RETURNING id
            """,
            (target_date, RESOURCE_ID, PARTICIPANT),
        )
        return cur.fetchone()["id"]


def finish_ingestion_run(
    conn,
    run_id: int,
    status: str,
    records_fetched: int,
    records_upserted: int,
    error_message: str = None,
) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE ingestion_runs
            SET status = %s,
                records_fetched = %s,
                records_upserted = %s,
                error_message = %s,
                finished_at = now()
            WHERE id = %s
            RETURNING *
            """,
            (status, records_fetched, records_upserted, error_message, run_id),
        )
        return serialize_row(cur.fetchone())


def upsert_results(conn, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with conn.cursor() as cur:
        for record in records:
            cur.execute(
                """
                INSERT INTO auction_results (
                  unit_result_id,
                  registered_auction_participant,
                  auction_unit,
                  service_type,
                  auction_product,
                  executed_quantity,
                  clearing_price,
                  delivery_start,
                  delivery_end,
                  technology_type,
                  post_code,
                  source_resource_id,
                  raw_json,
                  ingested_at
                )
                VALUES (
                  %(unit_result_id)s,
                  %(registered_auction_participant)s,
                  %(auction_unit)s,
                  %(service_type)s,
                  %(auction_product)s,
                  %(executed_quantity)s,
                  %(clearing_price)s,
                  %(delivery_start)s,
                  %(delivery_end)s,
                  %(technology_type)s,
                  %(post_code)s,
                  %(source_resource_id)s,
                  %(raw_json)s,
                  now()
                )
                ON CONFLICT (unit_result_id) DO UPDATE SET
                  registered_auction_participant = EXCLUDED.registered_auction_participant,
                  auction_unit = EXCLUDED.auction_unit,
                  service_type = EXCLUDED.service_type,
                  auction_product = EXCLUDED.auction_product,
                  executed_quantity = EXCLUDED.executed_quantity,
                  clearing_price = EXCLUDED.clearing_price,
                  delivery_start = EXCLUDED.delivery_start,
                  delivery_end = EXCLUDED.delivery_end,
                  technology_type = EXCLUDED.technology_type,
                  post_code = EXCLUDED.post_code,
                  source_resource_id = EXCLUDED.source_resource_id,
                  raw_json = EXCLUDED.raw_json,
                  ingested_at = now()
                """,
                {**record, "raw_json": Jsonb(record["raw_json"])},
            )
            count += 1
    return count


def list_results(
    target_date: date,
    service_type: str = None,
    auction_unit: str = None,
    auction_product: str = None,
    database_url: str = None,
) -> List[Dict[str, Any]]:
    start, end = day_bounds(target_date)
    filters = ["delivery_start >= %s", "delivery_start < %s"]
    params: List[Any] = [start, end]

    if service_type:
        filters.append("service_type = %s")
        params.append(service_type)
    if auction_unit:
        filters.append("auction_unit = %s")
        params.append(auction_unit)
    if auction_product:
        filters.append("auction_product = %s")
        params.append(auction_product)

    where_clause = " AND ".join(filters)
    with connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT *
                FROM auction_results
                WHERE {where_clause}
                ORDER BY delivery_start, auction_unit, auction_product
                """,
                params,
            )
            return [serialize_row(row) for row in cur.fetchall()]


def get_options(target_date: date, database_url: str = None) -> Dict[str, List[str]]:
    start, end = day_bounds(target_date)
    with connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                  array_remove(array_agg(DISTINCT service_type ORDER BY service_type), NULL) AS service_types,
                  array_remove(array_agg(DISTINCT auction_unit ORDER BY auction_unit), NULL) AS auction_units,
                  array_remove(array_agg(DISTINCT auction_product ORDER BY auction_product), NULL) AS auction_products
                FROM auction_results
                WHERE delivery_start >= %s AND delivery_start < %s
                """,
                (start, end),
            )
            row = cur.fetchone()
            return {
                "service_types": row["service_types"] or [],
                "auction_units": row["auction_units"] or [],
                "auction_products": row["auction_products"] or [],
            }


def get_summary(target_date: date, database_url: str = None) -> Dict[str, Any]:
    start, end = day_bounds(target_date)
    with connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                  COUNT(*)::int AS total_records,
                  COALESCE(SUM(executed_quantity), 0)::float AS total_executed_quantity,
                  COALESCE(AVG(clearing_price), 0)::float AS average_clearing_price
                FROM auction_results
                WHERE delivery_start >= %s AND delivery_start < %s
                """,
                (start, end),
            )
            totals = cur.fetchone()

            cur.execute(
                """
                SELECT service_type, SUM(executed_quantity)::float AS executed_quantity
                FROM auction_results
                WHERE delivery_start >= %s AND delivery_start < %s
                GROUP BY service_type
                ORDER BY service_type
                """,
                (start, end),
            )
            by_service_type = [serialize_row(row) for row in cur.fetchall()]

            cur.execute(
                """
                SELECT auction_unit, SUM(executed_quantity)::float AS executed_quantity
                FROM auction_results
                WHERE delivery_start >= %s AND delivery_start < %s
                GROUP BY auction_unit
                ORDER BY executed_quantity DESC, auction_unit
                """,
                (start, end),
            )
            by_auction_unit = [serialize_row(row) for row in cur.fetchall()]

    return {
        **serialize_row(totals),
        "by_service_type": by_service_type,
        "by_auction_unit": by_auction_unit,
    }


def day_bounds(target_date: date):
    start = datetime.combine(target_date, datetime.min.time())
    return start, start + timedelta(days=1)


def serialize_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None

    serialized = {}
    for key, value in row.items():
        if isinstance(value, (date, datetime)):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized
