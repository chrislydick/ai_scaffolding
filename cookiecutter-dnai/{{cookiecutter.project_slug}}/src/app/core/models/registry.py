"""Simple model registry routing by task.

Configured to use Bedrock by default. Future: AOAI mirror.
"""
from __future__ import annotations

from typing import Any

from .bedrock_client import BedrockClient


def get_model(task: str) -> Any:
    # Future: load config/models.yaml to map task->provider/model_id
    return BedrockClient()

