"""Athena TableIO via PyAthena.

Implements a minimal TableIO with read/write signatures.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os

import pandas as pd

try:
    from pyathena import connect
except Exception:  # pragma: no cover
    connect = None  # type: ignore


class TableIOProtocol:  # lightweight Protocol stand-in
    def read(self, name: str, where: Optional[Dict[str, Any]] = None) -> pd.DataFrame: ...
    def write(self, name: str, df: pd.DataFrame, mode: str = "append") -> None: ...


@dataclass
class AthenaIO(TableIOProtocol):
    region: Optional[str] = None
    workgroup: str = "primary"

    def __post_init__(self):
        self.region = self.region or os.getenv("AWS_REGION", "us-east-1")
        if connect is None:
            raise RuntimeError("pyathena not installed. Add 'pyathena' to dependencies.")
        self._conn = connect(region_name=self.region, work_group=self.workgroup)

    def read(self, name: str, where: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        where_clause = ""
        if where:
            parts = []
            for k, v in where.items():
                if isinstance(v, str):
                    parts.append(f"{k} = '{v}'")
                else:
                    parts.append(f"{k} = {v}")
            where_clause = " WHERE " + " AND ".join(parts)
        sql = f"SELECT * FROM {name}{where_clause} LIMIT 10000"
        return pd.read_sql(sql, self._conn)

    def write(self, name: str, df: pd.DataFrame, mode: str = "append") -> None:  # pragma: no cover - simplified
        raise NotImplementedError("Athena write is out-of-scope for minimal template.")

