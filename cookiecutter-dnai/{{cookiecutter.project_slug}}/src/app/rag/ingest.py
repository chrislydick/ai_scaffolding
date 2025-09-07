"""Minimal ingest stub: chunk -> embed -> push (placeholder).

This script demonstrates a simple embedding call to ensure the pipeline is wired.
"""
import glob
import os
from pathlib import Path

from src.app.core.models.bedrock_client import BedrockClient


def iter_docs(pattern: str):
    for path in glob.glob(pattern):
        with open(path, "rb") as f:
            yield Path(path).name, f.read().decode(errors="ignore")


def run(pattern: str = "data/kb/*"):
    print(f"[ingest] Loading docs from {pattern}")
    client = BedrockClient()
    texts = []
    for name, content in iter_docs(pattern):
        chunk = content[:2000]
        texts.append(chunk)
    if texts:
        print(f"[ingest] Embedding {len(texts)} chunks...")
        _ = client.embed(texts)
    print("[ingest] Done (demo).")


if __name__ == "__main__":
    pattern = os.getenv("KB_GLOB", "data/kb/*")
    run(pattern)

