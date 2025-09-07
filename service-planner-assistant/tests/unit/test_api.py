from src.app.api.handlers import lambda_handler
import json


def _api_event(path: str, method: str, body: dict | None = None, auth: str | None = None):
    return {
        "path": path,
        "httpMethod": method,
        "headers": {"Authorization": auth} if auth else {},
        "body": json.dumps(body or {}),
        "isBase64Encoded": False,
    }


def test_healthz():
    res = lambda_handler(_api_event("/healthz", "GET"), None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == {"status": "ok"}


def test_chat():
    res = lambda_handler(_api_event("/chat", "POST", {"q": "hello"}, auth="x"), None)
    assert res["statusCode"] == 200
    body = json.loads(res["body"]) 
    assert "answer" in body
