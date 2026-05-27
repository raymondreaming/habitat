from datetime import date, datetime
from pathlib import Path

from app.datasets import HABITAT_AUCTION_RESULTS
from app.neso_queries import build_daily_dataset_sql, build_market_totals_sql
from app.normalizers import normalize_auction_result, normalize_market_service_total


def test_build_habitat_sql_uses_validated_date_window():
    sql = build_daily_dataset_sql(HABITAT_AUCTION_RESULTS, date(2026, 5, 26))

    assert HABITAT_AUCTION_RESULTS.participant in sql
    assert "'2026-05-26T00:00:00'" in sql
    assert "'2026-05-27T00:00:00'" in sql


def test_build_market_service_totals_sql_groups_market_by_service():
    sql = build_market_totals_sql(HABITAT_AUCTION_RESULTS, date(2026, 5, 26))

    assert "GROUP BY \"serviceType\"" in sql
    assert "SUM(\"executedQuantity\")" in sql
    assert "'2026-05-26T00:00:00'" in sql


def test_normalize_record_parses_sql_endpoint_numeric_strings():
    row = {
        "registeredAuctionParticipant": HABITAT_AUCTION_RESULTS.participant,
        "auctionUnit": "OCHLB-1",
        "serviceType": "Quick Reserve",
        "auctionProduct": "NQR",
        "executedQuantity": "14.0",
        "clearingPrice": "0.27",
        "deliveryStart": "2026-05-26T00:00:00",
        "deliveryEnd": "2026-05-26T00:30:00",
        "technologyType": "Batteries",
        "postCode": "DY4 0PY",
        "unitResultID": "2730#||#2047#||#NQR#||#168384",
    }

    normalized = normalize_auction_result(row)

    assert normalized["unit_result_id"] == "2730#||#2047#||#NQR#||#168384"
    assert normalized["executed_quantity"] == 14.0
    assert normalized["clearing_price"] == 0.27
    assert normalized["delivery_start"] == datetime(2026, 5, 26, 0, 0)


def test_normalize_market_service_total_parses_aggregate_strings():
    row = {
        "serviceType": "Quick Reserve",
        "total_records": "2035",
        "total_executed_quantity": "36450.0",
        "average_clearing_price": "2.7582063882063882",
    }

    normalized = normalize_market_service_total(row, date(2026, 5, 26))

    assert normalized["target_date"] == date(2026, 5, 26)
    assert normalized["service_type"] == "Quick Reserve"
    assert normalized["total_records"] == 2035
    assert normalized["total_executed_quantity"] == 36450.0


def test_frontend_does_not_reference_neso_api():
    repo_root = Path(__file__).resolve().parents[2]
    frontend_files = repo_root.joinpath("frontend", "src").rglob("*")
    source_text = "\n".join(path.read_text() for path in frontend_files if path.is_file())

    assert "api.neso.energy" not in source_text
    assert "datastore_search" not in source_text


def test_repository_reads_do_not_import_neso_client():
    repo_root = Path(__file__).resolve().parents[2]
    repository_source = repo_root.joinpath("backend", "app", "repository.py").read_text()

    assert "NesoClient" not in repository_source
    assert "neso_client" not in repository_source
