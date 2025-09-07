from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from .auth import verify_request

app = FastAPI(title="{{ cookiecutter.project_name }}")


class ChatRequest(BaseModel):
    q: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[str] = []


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, authorization: Optional[str] = Header(None)):
    if not verify_request(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")

    {% if cookiecutter.cloud == 'aws' %}
    try:
        from src.app.core.models.bedrock_client import BedrockClient
    except Exception as ex:  # pragma: no cover - import fallback
        return ChatResponse(answer=f"Local mode: {req.q}", citations=[])

    client = BedrockClient()
    answer = client.generate(task="rag", prompt=req.q, context_docs=[])
    return ChatResponse(answer=answer, citations=[])
    {% else %}
    # Azure path (future): use AOAI client when available
    return ChatResponse(answer=f"Echo: {req.q}", citations=[])
    {% endif %}

