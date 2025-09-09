"""Feature builders (stubs)."""
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include=["number"]).columns:
        df[f"{col}_z"] = (df[col] - df[col].mean()) / (df[col].std() + 1e-9)
    return df

