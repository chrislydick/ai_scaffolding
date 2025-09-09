"""Azure Purview client (lightweight) for catalog/MDM hooks."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests


SCOPE = "https://purview.azure.net/.default"


def _get_token() -> Optional[str]:
    try:
        from azure.identity import DefaultAzureCredential  # type: ignore

        cred = DefaultAzureCredential()
        token = cred.get_token(SCOPE)
        return token.token
    except Exception:
        return os.getenv("AZURE_ACCESS_TOKEN")


def _endpoint() -> Optional[str]:
    acct = os.getenv("AZURE_PURVIEW_ACCOUNT")
    if not acct:
        return None
    return f"https://{acct}.purview.azure.com"


def _headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def register_s3_asset(name: str, s3_uri: str, collection: Optional[str] = None) -> bool:
    ep = _endpoint()
    tok = _get_token()
    if not (ep and tok):
        return False
    url = f"{ep}/catalog/api/atlas/v2/entity"
    entity = {
        "entity": {
            "typeName": "aws_s3_object",
            "attributes": {
                "name": name,
                "qualifiedName": s3_uri,
            },
            "collectionId": collection,
        }
    }
    r = requests.post(url, headers=_headers(tok), data=json.dumps(entity), timeout=15)
    return r.ok


def upsert_glossary_term(glossary_name: str, term: str, definition: str) -> bool:
    ep = _endpoint()
    tok = _get_token()
    if not (ep and tok):
        return False
    url = f"{ep}/catalog/api/glossary/terms"
    payload = {
        "name": term,
        "shortDescription": definition[:200],
        "longDescription": definition,
        "anchor": {"glossaryGuid": glossary_name},
    }
    r = requests.post(url, headers=_headers(tok), data=json.dumps(payload), timeout=15)
    return r.ok

