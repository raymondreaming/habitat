import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from app import database
from app.auth import require_ingest_api_key
from app.config import get_config
from app.dates import resolve_target_date
from app.ingestion_service import IngestionService
from app.repository import AuctionResultsRepository


config = get_config()
repository = AuctionResultsRepository(config.database_url)
ingestion_service = IngestionService(repository=repository)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        database.init_db(config.database_url)
    except Exception:
        logger.exception("Database initialization failed during startup")
    yield


app = FastAPI(title="Habitat Auction Results API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/ingest")
def ingest_endpoint(request: Request, date: Optional[str] = Query(default=None)):
    require_ingest_api_key(request, config.ingest_api_key)
    target_date = parse_date_or_400(date)
    try:
        return ingestion_service.ingest_date(target_date, config.database_url)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# Contract: read endpoints below query Postgres through the repository only.
# NESO HTTP access is intentionally isolated to ingestion_service -> neso_client.
@app.get("/api/results")
def results_endpoint(
    date: Optional[str] = Query(default=None),
    service_type: Optional[str] = Query(default=None),
    auction_unit: Optional[str] = Query(default=None),
    auction_product: Optional[str] = Query(default=None),
):
    target_date = parse_date_or_400(date)
    return {
        "date": target_date.isoformat(),
        "results": repository.list_results(
            target_date=target_date,
            service_type=service_type,
            auction_unit=auction_unit,
            auction_product=auction_product,
        ),
    }


@app.get("/api/options")
def options_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), **repository.get_options(target_date)}


@app.get("/api/summary")
def summary_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), **repository.get_summary(target_date)}


@app.get("/api/market-share")
def market_share_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), "market_share": repository.get_market_share(target_date)}


@app.get("/api/timeseries")
def timeseries_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), "timeseries": repository.get_timeseries(target_date)}


@app.get("/api/units")
def units_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), "units": repository.get_units(target_date)}


@app.get("/api/products")
def products_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), "products": repository.get_products(target_date)}


@app.get("/api/latest-date")
def latest_date_endpoint():
    return {"date": repository.get_latest_delivery_date()}


@app.get("/api/dates")
def dates_endpoint():
    return {"dates": repository.list_delivery_dates()}


def parse_date_or_400(value: Optional[str]):
    try:
        return resolve_target_date(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
