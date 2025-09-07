"""Simple PII redaction helpers."""
import re
from typing import Dict, Any


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def redact_payload(payload: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - stub
    text = str(payload)
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    return {"redacted": text}

