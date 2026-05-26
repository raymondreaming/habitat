from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Tuple


@dataclass(frozen=True)
class NesoDataset:
    name: str
    resource_id: str
    participant: str
    participant_field: str
    delivery_start_field: str
    order_by: Tuple[str, ...]

    def build_daily_sql(self, target_date: date) -> str:
        start = datetime.combine(target_date, datetime.min.time())
        end = start + timedelta(days=1)
        start_text = start.isoformat(timespec="seconds")
        end_text = end.isoformat(timespec="seconds")
        order_clause = ", ".join(quote_identifier(field) for field in self.order_by)

        return f"""
SELECT *
FROM "{self.resource_id}"
WHERE {quote_identifier(self.participant_field)} = '{self.participant}'
  AND {quote_identifier(self.delivery_start_field)} >= '{start_text}'
  AND {quote_identifier(self.delivery_start_field)} < '{end_text}'
ORDER BY {order_clause}
""".strip()

    def build_market_service_totals_sql(self, target_date: date) -> str:
        start = datetime.combine(target_date, datetime.min.time())
        end = start + timedelta(days=1)
        start_text = start.isoformat(timespec="seconds")
        end_text = end.isoformat(timespec="seconds")

        return f"""
SELECT
  "serviceType",
  COUNT(*) AS total_records,
  SUM("executedQuantity") AS total_executed_quantity,
  AVG("clearingPrice") AS average_clearing_price
FROM "{self.resource_id}"
WHERE {quote_identifier(self.delivery_start_field)} >= '{start_text}'
  AND {quote_identifier(self.delivery_start_field)} < '{end_text}'
GROUP BY "serviceType"
ORDER BY "serviceType"
""".strip()


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


HABITAT_AUCTION_RESULTS = NesoDataset(
    name="habitat_auction_results",
    resource_id="a63ab354-7e68-44c2-ad96-c6f920c30e85",
    participant="HABITAT ENERGY LIMITED",
    participant_field="registeredAuctionParticipant",
    delivery_start_field="deliveryStart",
    order_by=("deliveryStart", "auctionUnit", "auctionProduct"),
)
