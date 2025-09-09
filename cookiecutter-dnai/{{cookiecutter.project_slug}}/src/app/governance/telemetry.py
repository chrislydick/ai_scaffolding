"""Telemetry stub: print-based tracing."""
from contextlib import contextmanager
from time import time


@contextmanager
def span(name: str):  # pragma: no cover - stub
    t0 = time()
    try:
        yield
    finally:
        dur = (time() - t0) * 1000
        print(f"[telemetry] {name} took {dur:.1f} ms")

