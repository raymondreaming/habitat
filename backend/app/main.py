from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app import db
from app.config import get_config
from app.dates import resolve_target_date
from app.ingestion import ingest


config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db(config.database_url)
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
def ingest_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    try:
        return ingest(target_date, config.database_url)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


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
        "results": db.list_results(
            target_date=target_date,
            service_type=service_type,
            auction_unit=auction_unit,
            auction_product=auction_product,
            database_url=config.database_url,
        ),
    }


@app.get("/api/options")
def options_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), **db.get_options(target_date, config.database_url)}


@app.get("/api/summary")
def summary_endpoint(date: Optional[str] = Query(default=None)):
    target_date = parse_date_or_400(date)
    return {"date": target_date.isoformat(), **db.get_summary(target_date, config.database_url)}


def parse_date_or_400(value: Optional[str]):
    try:
        return resolve_target_date(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
