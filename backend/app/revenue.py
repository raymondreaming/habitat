GROSS_REVENUE_SQL = "executed_quantity * clearing_price * EXTRACT(EPOCH FROM (delivery_end - delivery_start)) / 3600.0"


def sum_gross_revenue_sql() -> str:
    return f"SUM({GROSS_REVENUE_SQL})::float"


def coalesced_sum_gross_revenue_sql() -> str:
    return f"COALESCE(SUM({GROSS_REVENUE_SQL}), 0)::float"
