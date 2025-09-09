"""Lambda-style HTTP handlers for API Gateway events.

No FastAPI or Docker used; routes are dispatched by path/method.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from .auth import verify_request


def _response(status: int, body: Dict[str, Any]):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _healthz(event: Dict[str, Any]):
    return _response(200, {"status": "ok"})


def _chat(event: Dict[str, Any]):
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    auth = headers.get("authorization")
    if not verify_request(auth):
        return _response(401, {"message": "Unauthorized"})

    try:
        body = json.loads(event.get("body") or "{}")
    except Exception:
        body = {}
    q = body.get("q", "")

    {% if cookiecutter.cloud == 'aws' %}
    try:
        from src.app.core.models.bedrock_client import BedrockClient

        client = BedrockClient()
        answer = client.generate(task="rag", prompt=q, context_docs=[])
        return _response(200, {"answer": answer, "citations": []})
    except Exception:
        # Local fallback when AWS creds/models unavailable
        return _response(200, {"answer": f"Local mode: {q}", "citations": []})
    {% else %}
    return _response(200, {"answer": f"Echo: {q}", "citations": []})
    {% endif %}


def lambda_handler(event: Dict[str, Any], context: Any):
    path = event.get("path", "/")
    method = (event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method") or "").upper()
    if path == "/healthz" and method in ("GET", ""):
        return _healthz(event)
    if path == "/chat" and method == "POST":
        return _chat(event)
    return _response(404, {"message": "Not Found"})
