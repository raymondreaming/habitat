from datetime import datetime
from typing import Any, Dict, Optional


class NesoDataError(RuntimeError):
    pass


def require_text(record: Dict[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None or str(value).strip() == "":
        raise NesoDataError(f"missing required NESO field: {key}")
    return str(value)


def optional_text(value: Any) -> Optional[str]:
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
