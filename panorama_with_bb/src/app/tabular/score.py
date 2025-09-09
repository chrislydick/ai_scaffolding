"""Batch scoring stub."""
import pandas as pd

from .features import build_features


def score():  # pragma: no cover - stub
    df = pd.DataFrame({"x": [1, 2, 3]})
    feats = build_features(df)
    feats["score"] = 0.5
    print(feats)


if __name__ == "__main__":
    score()

