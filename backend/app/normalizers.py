from datetime import datetime
from datetime import date
from typing import Any, Dict

from app.datasets import HABITAT_AUCTION_RESULTS, NesoDataset


class NesoDataError(RuntimeError):
    pass


def normalize_auction_result(
    record: Dict[str, Any],
    dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
) -> Dict[str, Any]:
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
        "source_resource_id": dataset.resource_id,
        "raw_json": record,
    }


def normalize_market_service_total(
    record: Dict[str, Any],
    target_date: date,
    dataset: NesoDataset = HABITAT_AUCTION_RESULTS,
) -> Dict[str, Any]:
    return {
        "target_date": target_date,
        "source_resource_id": dataset.resource_id,
        "service_type": require_text(record, "serviceType"),
        "total_records": parse_int(record, "total_records"),
        "total_executed_quantity": parse_float(record, "total_executed_quantity"),
        "average_clearing_price": parse_float(record, "average_clearing_price"),
        "raw_json": record,
    }


def require_text(record: Dict[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None or str(value).strip() == "":
        raise NesoDataError(f"missing required NESO field: {key}")
    return str(value)


def optional_text(value: Any) -> str:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_float(record: Dict[str, Any], key: str) -> float:
    value = record.get(key)
    if value is None:
        raise NesoDataError(f"missing required numeric NESO field: {key}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise NesoDataError(f"invalid numeric NESO field {key}: {value}") from exc


def parse_int(record: Dict[str, Any], key: str) -> int:
    value = record.get(key)
    if value is None:
        raise NesoDataError(f"missing required integer NESO field: {key}")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise NesoDataError(f"invalid integer NESO field {key}: {value}") from exc


def parse_timestamp(record: Dict[str, Any], key: str) -> datetime:
    value = record.get(key)
    if value is None:
        raise NesoDataError(f"missing required timestamp NESO field: {key}")
    try:
        return datetime.fromisoformat(str(value))
    except ValueError as exc:
        raise NesoDataError(f"invalid timestamp NESO field {key}: {value}") from exc
