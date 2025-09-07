"""Minimal retrieve stub (placeholder)."""

from typing import List


def retrieve(query: str, top_k: int = 3, filters: dict | None = None) -> List[str]:
    return [f"Doc snippet {i+1} for: {query}" for i in range(top_k)]

