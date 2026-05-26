from typing import Optional

from fastapi import HTTPException, Request, status


def require_ingest_api_key(request: Request, configured_api_key: Optional[str]) -> None:
    if not configured_api_key:
        return

    supplied_key = request.headers.get("x-api-key")
    if supplied_key != configured_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
        )
