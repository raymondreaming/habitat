from datetime import date, datetime
from zoneinfo import ZoneInfo


UK_TIMEZONE = ZoneInfo("Europe/London")


def current_uk_date() -> date:
    return datetime.now(tz=UK_TIMEZONE).date()


def parse_target_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD format") from exc


def resolve_target_date(value: str = None) -> date:
    if value:
        return parse_target_date(value)
    return current_uk_date()
