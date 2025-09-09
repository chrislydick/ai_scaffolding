"""
SAP BW / HANA adapter (on‑prem) — limited support.

Notes
- This adapter avoids hard dependencies on SAP proprietary clients.
- For SQL access, install one of:
  - SAP HANA client (hdbcli) and SQLAlchemy dialect
  - "sqlalchemy-hana" if available for your platform
- For BW OData, expose an OData service and use requests/pyodata.

Configuration (example .env or settings)
- SAP_HOST, SAP_PORT, SAP_USER, SAP_PASSWORD, SAP_SCHEMA
- Or for OData: SAP_ODATA_BASE_URL, SAP_ODATA_AUTH (optional)
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


def _make_sqlalchemy_engine() -> Any:
    try:
        from sqlalchemy import create_engine
    except Exception as ex:
        raise RuntimeError("sqlalchemy not installed; cannot use SAP HANA SQL access") from ex

    import os
    host = os.getenv("SAP_HOST") or "localhost"
    port = os.getenv("SAP_PORT") or "30015"
    user = os.getenv("SAP_USER") or "SYSTEM"
    pwd = os.getenv("SAP_PASSWORD") or ""

    # Prefer hdbcli if available
    try:
        import hdbcli  # type: ignore
        uri = f"hana+hdbcli://{user}:{pwd}@{host}:{port}"
        return create_engine(uri)
    except Exception:
        pass

    # Fallback: sqlalchemy-hana dialect
    try:
        uri = f"hana://{user}:{pwd}@{host}:{port}"
        return create_engine(uri)
    except Exception as ex:
        raise RuntimeError("No suitable SAP HANA SQLAlchemy dialect found (hdbcli or sqlalchemy-hana)") from ex


def query(sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Run a SQL query against HANA and return list of dict rows.

    Requires SQLAlchemy + HANA driver available at runtime.
    """
    eng = _make_sqlalchemy_engine()
    with eng.connect() as conn:
        result = conn.execute(sql, params or {})
        cols = result.keys()
        return [dict(zip(cols, row)) for row in result.fetchall()]


def odata_get(entity_set: str, base_url: Optional[str] = None, auth: Optional[str] = None, **query_params: Any) -> Dict[str, Any]:
    """Fetch from SAP BW OData service.

    Provide SAP_ODATA_BASE_URL and optional SAP_ODATA_AUTH (e.g., Basic token) via env or args.
    """
    import os
    import requests

    base = base_url or os.getenv("SAP_ODATA_BASE_URL")
    if not base:
        raise RuntimeError("SAP_ODATA_BASE_URL not set")
    url = base.rstrip("/") + f"/{entity_set}"
    headers = {"Accept": "application/json"}
    token = auth or os.getenv("SAP_ODATA_AUTH")
    if token:
        headers["Authorization"] = token
    resp = requests.get(url, params=query_params, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


__all__ = [
    "query",
    "odata_get",
]

