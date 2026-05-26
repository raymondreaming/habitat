from typing import Any, Dict, List

import httpx


NESO_SQL_ENDPOINT = "https://api.neso.energy/api/3/action/datastore_search_sql"


class NesoClientError(RuntimeError):
    pass


class NesoClient:
    def __init__(self, sql_endpoint: str = NESO_SQL_ENDPOINT, timeout: float = 30.0):
        self.sql_endpoint = sql_endpoint
        self.timeout = timeout

    def search_sql(self, sql: str) -> List[Dict[str, Any]]:
        try:
            response = httpx.get(self.sql_endpoint, params={"sql": sql}, timeout=self.timeout)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise NesoClientError(f"NESO request failed: {exc}") from exc

        payload = response.json()
        if not payload.get("success"):
            raise NesoClientError(f"NESO returned an error: {payload.get('error')}")

        records = payload.get("result", {}).get("records", [])
        if not isinstance(records, list):
            raise NesoClientError("NESO response did not contain a record list")
        return records
