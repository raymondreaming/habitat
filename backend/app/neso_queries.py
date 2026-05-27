from datetime import date, datetime, timedelta

from app.datasets import NesoDataset


def build_daily_dataset_sql(dataset: NesoDataset, target_date: date) -> str:
    start_text, end_text = delivery_day_window(target_date)
    order_clause = ", ".join(quote_identifier(field) for field in dataset.order_by)

    return f"""
SELECT *
FROM {quote_identifier(dataset.resource_id)}
WHERE {quote_identifier(dataset.participant_field)} = {quote_literal(dataset.participant)}
  AND {quote_identifier(dataset.delivery_start_field)} >= {quote_literal(start_text)}
  AND {quote_identifier(dataset.delivery_start_field)} < {quote_literal(end_text)}
ORDER BY {order_clause}
""".strip()


def build_market_totals_sql(dataset: NesoDataset, target_date: date) -> str:
    if dataset.market_totals is None:
        raise ValueError(f"dataset has no market totals configuration: {dataset.name}")

    start_text, end_text = delivery_day_window(target_date)
    totals = dataset.market_totals
    group_field = quote_identifier(totals.group_field)

    return f"""
SELECT
  {group_field},
  COUNT(*) AS total_records,
  SUM({quote_identifier(totals.quantity_field)}) AS total_executed_quantity,
  AVG({quote_identifier(totals.price_field)}) AS average_clearing_price
FROM {quote_identifier(dataset.resource_id)}
WHERE {quote_identifier(dataset.delivery_start_field)} >= {quote_literal(start_text)}
  AND {quote_identifier(dataset.delivery_start_field)} < {quote_literal(end_text)}
GROUP BY {group_field}
ORDER BY {group_field}
""".strip()


def delivery_day_window(target_date: date) -> tuple[str, str]:
    start = datetime.combine(target_date, datetime.min.time())
    end = start + timedelta(days=1)
    return start.isoformat(timespec="seconds"), end.isoformat(timespec="seconds")


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def quote_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
