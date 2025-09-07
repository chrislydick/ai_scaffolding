from fastapi.testclient import TestClient
from src.app.api.handlers import app


client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat():
    r = client.post("/chat", json={"q": "hello"}, headers={"Authorization": "test"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body

