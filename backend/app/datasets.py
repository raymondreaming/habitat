from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class MarketTotalsConfig:
    group_field: str
    quantity_field: str
    price_field: str


@dataclass(frozen=True)
class NesoDataset:
    name: str
    resource_id: str
    participant: str
    participant_field: str
    delivery_start_field: str
    unique_key_field: str
    order_by: Tuple[str, ...]
    market_totals: Optional[MarketTotalsConfig] = None



HABITAT_AUCTION_RESULTS = NesoDataset(
    name="habitat_auction_results",
    resource_id="a63ab354-7e68-44c2-ad96-c6f920c30e85",
    participant="HABITAT ENERGY LIMITED",
    participant_field="registeredAuctionParticipant",
    delivery_start_field="deliveryStart",
    unique_key_field="unitResultID",
    order_by=("deliveryStart", "auctionUnit", "auctionProduct"),
    market_totals=MarketTotalsConfig(
        group_field="serviceType",
        quantity_field="executedQuantity",
        price_field="clearingPrice",
    ),
)

DATASETS: Dict[str, NesoDataset] = {
    HABITAT_AUCTION_RESULTS.name: HABITAT_AUCTION_RESULTS,
}
