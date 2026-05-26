from datetime import date
from typing import Any, Callable, Dict, Optional

from app import database
from app.datasets import HABITAT_AUCTION_RESULTS, NesoDataset
from app.neso_client import NesoClient
from app.normalizers import normalize_auction_result, normalize_market_service_total
from app.repository import AuctionResultsRepository


class IngestionService:
    def __init__(
        self,
        client: Optional[NesoClient] = None,
        repository: Optional[AuctionResultsRepository] = None,
        dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
        normalizer: Callable = normalize_auction_result,
    ):
        self.client = client or NesoClient()
        self.repository = repository or AuctionResultsRepository()
        self.dataset = dataset
        self.normalizer = normalizer

    def ingest_date(self, target_date: date, database_url: Optional[str] = None) -> Dict[str, Any]:
        database.init_db(database_url)

        with database.connect(database_url) as conn:
            run_id = self.repository.create_ingestion_run(conn, target_date, self.dataset)
            conn.commit()
            try:
                sql = self.dataset.build_daily_sql(target_date)
                raw_records = self.client.search_sql(sql)
                records = [self.normalizer(record, self.dataset) for record in raw_records]
                upserted = self.repository.upsert_results(conn, records)
                market_sql = self.dataset.build_market_service_totals_sql(target_date)
                raw_market_totals = self.client.search_sql(market_sql)
                market_totals = [
                    normalize_market_service_total(record, target_date, self.dataset)
                    for record in raw_market_totals
                ]
                self.repository.upsert_market_service_totals(conn, market_totals)
                conn.commit()
            except Exception as exc:
                conn.rollback()
                run = self.repository.finish_ingestion_run(
                    conn=conn,
                    run_id=run_id,
                    status="failed",
                    records_fetched=0,
                    records_upserted=0,
                    error_message=str(exc),
                )
                conn.commit()
                raise RuntimeError(run["error_message"]) from exc

            run = self.repository.finish_ingestion_run(
                conn=conn,
                run_id=run_id,
                status="succeeded",
                records_fetched=len(raw_records),
                records_upserted=upserted,
            )
            conn.commit()

        return run


def ingest_habitat_results(target_date: date, database_url: Optional[str] = None) -> Dict[str, Any]:
    repository = AuctionResultsRepository(database_url)
    return IngestionService(repository=repository).ingest_date(target_date, database_url)
