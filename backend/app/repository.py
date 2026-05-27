from datetime import date, datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

from psycopg.types.json import Jsonb

from app import database
from app.datasets import HABITAT_AUCTION_RESULTS, NesoDataset
from app.revenue import coalesced_sum_gross_revenue_sql, sum_gross_revenue_sql


class AuctionResultsRepository:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url

    def create_ingestion_run(self, conn, target_date: date, dataset: NesoDataset) -> int:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ingestion_runs (target_date, source_resource_id, participant, status)
                VALUES (%s, %s, %s, 'running')
                RETURNING id
                """,
                (target_date, dataset.resource_id, dataset.participant),
            )
            return cur.fetchone()["id"]

    def finish_ingestion_run(
        self,
        conn,
        run_id: int,
        status: str,
        records_fetched: int,
        records_upserted: int,
        error_message: Optional[str] = None,
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

    def upsert_results(self, conn, records: Iterable[Dict[str, Any]]) -> int:
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

    def upsert_market_service_totals(self, conn, records: Iterable[Dict[str, Any]]) -> int:
        count = 0
        with conn.cursor() as cur:
            for record in records:
                cur.execute(
                    """
                    INSERT INTO market_service_totals (
                      target_date,
                      source_resource_id,
                      service_type,
                      total_records,
                      total_executed_quantity,
                      average_clearing_price,
                      raw_json,
                      updated_at
                    )
                    VALUES (
                      %(target_date)s,
                      %(source_resource_id)s,
                      %(service_type)s,
                      %(total_records)s,
                      %(total_executed_quantity)s,
                      %(average_clearing_price)s,
                      %(raw_json)s,
                      now()
                    )
                    ON CONFLICT (target_date, source_resource_id, service_type) DO UPDATE SET
                      total_records = EXCLUDED.total_records,
                      total_executed_quantity = EXCLUDED.total_executed_quantity,
                      average_clearing_price = EXCLUDED.average_clearing_price,
                      raw_json = EXCLUDED.raw_json,
                      updated_at = now()
                    """,
                    {**record, "raw_json": Jsonb(record["raw_json"])},
                )
                count += 1
        return count

    def list_results(
        self,
        target_date: date,
        service_type: Optional[str] = None,
        auction_unit: Optional[str] = None,
        auction_product: Optional[str] = None,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[Dict[str, Any]]:
        start, end = day_bounds(target_date)
        filters = ["source_resource_id = %s", "delivery_start >= %s", "delivery_start < %s"]
        params: List[Any] = [dataset.resource_id, start, end]

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
        with database.connect(self.database_url) as conn:
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

    def get_options(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> Dict[str, List[str]]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                      array_remove(array_agg(DISTINCT service_type ORDER BY service_type), NULL) AS service_types,
                      array_remove(array_agg(DISTINCT auction_unit ORDER BY auction_unit), NULL) AS auction_units,
                      array_remove(array_agg(DISTINCT auction_product ORDER BY auction_product), NULL) AS auction_products
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    """,
                    (dataset.resource_id, start, end),
                )
                row = cur.fetchone()
                return {
                    "service_types": row["service_types"] or [],
                    "auction_units": row["auction_units"] or [],
                    "auction_products": row["auction_products"] or [],
                }

    def get_summary(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> Dict[str, Any]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                      COUNT(*)::int AS total_records,
                      COALESCE(SUM(executed_quantity), 0)::float AS total_executed_quantity,
                      COALESCE(AVG(clearing_price), 0)::float AS average_clearing_price,
                      {coalesced_sum_gross_revenue_sql()} AS estimated_gross_revenue,
                      COUNT(DISTINCT auction_unit)::int AS active_units
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    """,
                    (dataset.resource_id, start, end),
                )
                totals = cur.fetchone()

                cur.execute(
                    """
                    SELECT service_type, SUM(executed_quantity)::float AS executed_quantity
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    GROUP BY service_type
                    ORDER BY service_type
                    """,
                    (dataset.resource_id, start, end),
                )
                by_service_type = [serialize_row(row) for row in cur.fetchall()]

                cur.execute(
                    """
                    SELECT auction_unit, SUM(executed_quantity)::float AS executed_quantity
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    GROUP BY auction_unit
                    ORDER BY executed_quantity DESC, auction_unit
                    """,
                    (dataset.resource_id, start, end),
                )
                by_auction_unit = [serialize_row(row) for row in cur.fetchall()]

                top_service_by_volume = by_service_type[0] if by_service_type else None
                if by_service_type:
                    top_service_by_volume = max(by_service_type, key=lambda row: row["executed_quantity"])
                top_unit_by_volume = by_auction_unit[0] if by_auction_unit else None

        return {
            **serialize_row(totals),
            "top_service_by_volume": top_service_by_volume,
            "top_unit_by_volume": top_unit_by_volume,
            "by_service_type": by_service_type,
            "by_auction_unit": by_auction_unit,
        }

    def get_market_share(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[Dict[str, Any]]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH habitat AS (
                      SELECT
                        service_type,
                        COUNT(*)::int AS habitat_records,
                        SUM(executed_quantity)::float AS habitat_executed_quantity,
                        AVG(clearing_price)::float AS habitat_average_clearing_price
                      FROM auction_results
                      WHERE source_resource_id = %s
                        AND delivery_start >= %s
                        AND delivery_start < %s
                      GROUP BY service_type
                    )
                    SELECT
                      market.service_type,
                      COALESCE(habitat.habitat_records, 0)::int AS habitat_records,
                      market.total_records AS market_records,
                      COALESCE(habitat.habitat_executed_quantity, 0)::float AS habitat_executed_quantity,
                      market.total_executed_quantity::float AS market_executed_quantity,
                      CASE
                        WHEN market.total_executed_quantity = 0 THEN 0
                        ELSE (COALESCE(habitat.habitat_executed_quantity, 0) / market.total_executed_quantity * 100)::float
                      END AS habitat_market_share_percent,
                      COALESCE(habitat.habitat_average_clearing_price, 0)::float AS habitat_average_clearing_price,
                      market.average_clearing_price::float AS market_average_clearing_price
                    FROM market_service_totals market
                    LEFT JOIN habitat ON habitat.service_type = market.service_type
                    WHERE market.target_date = %s
                      AND market.source_resource_id = %s
                    ORDER BY market.service_type
                    """,
                    (dataset.resource_id, start, end, target_date, dataset.resource_id),
                )
                return [serialize_row(row) for row in cur.fetchall()]

    def get_timeseries(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[Dict[str, Any]]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                      delivery_start,
                      delivery_end,
                      service_type,
                      auction_product,
                      COUNT(*)::int AS total_records,
                      SUM(executed_quantity)::float AS executed_quantity,
                      AVG(clearing_price)::float AS average_clearing_price,
                      {sum_gross_revenue_sql()} AS estimated_gross_revenue
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    GROUP BY delivery_start, delivery_end, service_type, auction_product
                    ORDER BY delivery_start, service_type, auction_product
                    """,
                    (dataset.resource_id, start, end),
                )
                return [serialize_row(row) for row in cur.fetchall()]

    def get_units(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[Dict[str, Any]]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                      auction_unit,
                      COUNT(*)::int AS total_records,
                      SUM(executed_quantity)::float AS executed_quantity,
                      AVG(clearing_price)::float AS average_clearing_price,
                      {sum_gross_revenue_sql()} AS estimated_gross_revenue,
                      array_remove(array_agg(DISTINCT service_type ORDER BY service_type), NULL) AS service_types,
                      array_remove(array_agg(DISTINCT auction_product ORDER BY auction_product), NULL) AS auction_products
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    GROUP BY auction_unit
                    ORDER BY estimated_gross_revenue DESC, executed_quantity DESC, auction_unit
                    """,
                    (dataset.resource_id, start, end),
                )
                return [serialize_row(row) for row in cur.fetchall()]

    def get_products(
        self,
        target_date: date,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[Dict[str, Any]]:
        start, end = day_bounds(target_date)
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT
                      service_type,
                      auction_product,
                      COUNT(*)::int AS total_records,
                      SUM(executed_quantity)::float AS executed_quantity,
                      AVG(clearing_price)::float AS average_clearing_price,
                      {sum_gross_revenue_sql()} AS estimated_gross_revenue
                    FROM auction_results
                    WHERE source_resource_id = %s
                      AND delivery_start >= %s
                      AND delivery_start < %s
                    GROUP BY service_type, auction_product
                    ORDER BY estimated_gross_revenue DESC, executed_quantity DESC, service_type, auction_product
                    """,
                    (dataset.resource_id, start, end),
                )
                return [serialize_row(row) for row in cur.fetchall()]

    def get_latest_delivery_date(
        self,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> Optional[str]:
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT MAX(delivery_start::date) AS latest_date
                    FROM auction_results
                    WHERE source_resource_id = %s
                    """,
                    (dataset.resource_id,),
                )
                row = cur.fetchone()
                latest_date = row["latest_date"] if row else None
                return latest_date.isoformat() if latest_date else None

    def list_delivery_dates(
        self,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
    ) -> List[str]:
        with database.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT delivery_start::date AS delivery_date
                    FROM auction_results
                    WHERE source_resource_id = %s
                    GROUP BY delivery_start::date
                    ORDER BY delivery_start::date DESC
                    """,
                    (dataset.resource_id,),
                )
                return [row["delivery_date"].isoformat() for row in cur.fetchall()]


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
