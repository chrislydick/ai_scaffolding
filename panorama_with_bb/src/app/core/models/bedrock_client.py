from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import List, Optional

import boto3


ANTHROPIC_VERSION = "bedrock-2023-05-31"


@dataclass
class BedrockClient:
    region: Optional[str] = None
    rag_model_id: Optional[str] = None

    def __post_init__(self):
        self.region = self.region or os.getenv("AWS_REGION", "us-east-1")
        self.rag_model_id = self.rag_model_id or os.getenv(
            "BEDROCK_RAG_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
        )
        self.runtime = boto3.client("bedrock-runtime", region_name=self.region)

    def generate(self, task: str, prompt: str, context_docs: Optional[List[str]] = None, guardrails: str = "standard") -> str:
        """Minimal text generation for RAG-like tasks using Claude 3.5 Sonnet."""
        system_prefix = "You are a helpful assistant."
        if context_docs:
            ctx = "\n\n".join(context_docs)
            prompt = f"Use the following context to answer succinctly with citations if possible.\n\nContext:\n{ctx}\n\nQuestion: {prompt}"
        body = {
            "anthropic_version": ANTHROPIC_VERSION,
            "max_tokens": 512,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{system_prefix}\n\n{prompt}"},
                    ],
                }
            ],
        }
        resp = self.runtime.invoke_model(
            modelId=self.rag_model_id,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json",
        )
        payload = json.loads(resp["body"].read().decode("utf-8"))
        # Anthropic messages returns content list with text
        content = payload.get("content", [])
        if content and isinstance(content, list) and "text" in content[0]:
            return content[0]["text"]
        # Fallback to consolidated text
        return payload.get("output_text") or json.dumps(payload)

    def classify(self, text: str, labels: List[str]) -> str:
        prompt = f"Classify the following text into one of: {', '.join(labels)}. Text: {text}"
        return self.generate(task="classify", prompt=prompt)

    def embed(self, texts: List[str]) -> List[List[float]]:
        model_id = os.getenv("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0")
        out: List[List[float]] = []
        for t in texts:
            body = {"inputText": t}
            resp = self.runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                accept="application/json",
                contentType="application/json",
            )
            payload = json.loads(resp["body"].read().decode("utf-8"))
            vec = payload.get("embedding") or payload.get("embeddings", {}).get("values")
            out.append(vec or [])
        return out

