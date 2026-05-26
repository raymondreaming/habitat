from datetime import date
from typing import Any, Dict

from app import db
from app.neso import fetch_habitat_records


def ingest(target_date: date, database_url: str = None) -> Dict[str, Any]:
    db.init_db(database_url)

    with db.connect(database_url) as conn:
        run_id = db.create_ingestion_run(conn, target_date)
        conn.commit()
        try:
            records = fetch_habitat_records(target_date)
            upserted = db.upsert_results(conn, records)
            conn.commit()
        except Exception as exc:
            conn.rollback()
            run = db.finish_ingestion_run(
                conn=conn,
                run_id=run_id,
                status="failed",
                records_fetched=0,
                records_upserted=0,
                error_message=str(exc),
            )
            conn.commit()
            raise RuntimeError(run["error_message"]) from exc

        run = db.finish_ingestion_run(
            conn=conn,
            run_id=run_id,
            status="succeeded",
            records_fetched=len(records),
            records_upserted=upserted,
        )
        conn.commit()

    return run
