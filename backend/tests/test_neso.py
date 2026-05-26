from datetime import date, datetime

from app.neso import PARTICIPANT, build_habitat_sql, normalize_record


def test_build_habitat_sql_uses_validated_date_window():
    sql = build_habitat_sql(date(2026, 5, 26))

    assert PARTICIPANT in sql
    assert "'2026-05-26T00:00:00'" in sql
    assert "'2026-05-27T00:00:00'" in sql


def test_normalize_record_parses_sql_endpoint_numeric_strings():
    row = {
        "registeredAuctionParticipant": PARTICIPANT,
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

    normalized = normalize_record(row)

    assert normalized["unit_result_id"] == "2730#||#2047#||#NQR#||#168384"
    assert normalized["executed_quantity"] == 14.0
    assert normalized["clearing_price"] == 0.27
    assert normalized["delivery_start"] == datetime(2026, 5, 26, 0, 0)
