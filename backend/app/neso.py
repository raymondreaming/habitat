from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import httpx


NESO_SQL_ENDPOINT = "https://api.neso.energy/api/3/action/datastore_search_sql"
RESOURCE_ID = "a63ab354-7e68-44c2-ad96-c6f920c30e85"
PARTICIPANT = "HABITAT ENERGY LIMITED"


class NesoClientError(RuntimeError):
    pass


def build_habitat_sql(target_date: date) -> str:
    start = datetime.combine(target_date, datetime.min.time())
    end = start + timedelta(days=1)
    start_text = start.isoformat(timespec="seconds")
    end_text = end.isoformat(timespec="seconds")

    return f"""
SELECT *
FROM "{RESOURCE_ID}"
WHERE "registeredAuctionParticipant" = '{PARTICIPANT}'
  AND "deliveryStart" >= '{start_text}'
  AND "deliveryStart" < '{end_text}'
ORDER BY "deliveryStart", "auctionUnit", "auctionProduct"
""".strip()


def fetch_habitat_records(target_date: date) -> List[Dict[str, Any]]:
    sql = build_habitat_sql(target_date)
    try:
        response = httpx.get(NESO_SQL_ENDPOINT, params={"sql": sql}, timeout=30.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise NesoClientError(f"NESO request failed: {exc}") from exc

    payload = response.json()
    if not payload.get("success"):
        raise NesoClientError(f"NESO returned an error: {payload.get('error')}")

    records = payload.get("result", {}).get("records", [])
    return [normalize_record(record) for record in records]


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    unit_result_id = require_text(record, "unitResultID")
    return {
        "unit_result_id": unit_result_id,
        "registered_auction_participant": require_text(record, "registeredAuctionParticipant"),
        "auction_unit": require_text(record, "auctionUnit"),
        "service_type": require_text(record, "serviceType"),
        "auction_product": require_text(record, "auctionProduct"),
        "executed_quantity": parse_float(record, "executedQuantity"),
        "clearing_price": parse_float(record, "clearingPrice"),
        "delivery_start": parse_timestamp(record, "deliveryStart"),
        "delivery_end": parse_timestamp(record, "deliveryEnd"),
        "technology_type": optional_text(record.get("technologyType")),
        "post_code": optional_text(record.get("postCode")),
        "source_resource_id": RESOURCE_ID,
        "raw_json": record,
    }


def require_text(record: Dict[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None or str(value).strip() == "":
        raise NesoClientError(f"missing required NESO field: {key}")
    return str(value)


def optional_text(value: Any) -> str:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_float(record: Dict[str, Any], key: str) -> float:
    value = record.get(key)
    if value is None:
        raise NesoClientError(f"missing required numeric NESO field: {key}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise NesoClientError(f"invalid numeric NESO field {key}: {value}") from exc


def parse_timestamp(record: Dict[str, Any], key: str) -> datetime:
    value = record.get(key)
    if value is None:
        raise NesoClientError(f"missing required timestamp NESO field: {key}")
    try:
        return datetime.fromisoformat(str(value))
    except ValueError as exc:
        raise NesoClientError(f"invalid timestamp NESO field {key}: {value}") from exc
