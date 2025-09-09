"""S3 IO helpers: small JSON/CSV + presigned URLs."""
from __future__ import annotations

import io
import json
import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3
import pandas as pd


@dataclass
class S3IO:
    bucket: str
    region: Optional[str] = None

    def __post_init__(self):
        self.region = self.region or os.getenv("AWS_REGION", "us-east-1")
        self.s3 = boto3.client("s3", region_name=self.region)

    def put_json(self, key: str, obj: Any) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType="application/json")

    def get_json(self, key: str) -> Any:
        resp = self.s3.get_object(Bucket=self.bucket, Key=key)
        return json.loads(resp["Body"].read().decode("utf-8"))

    def put_csv(self, key: str, df: pd.DataFrame, index: bool = False) -> None:
        buf = io.StringIO()
        df.to_csv(buf, index=index)
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=buf.getvalue().encode("utf-8"), ContentType="text/csv")

    def get_csv(self, key: str) -> pd.DataFrame:
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return pd.read_csv(io.BytesIO(obj["Body"].read()))

    def presigned_url(self, key: str, method: str = "get_object", expires_in: int = 900) -> str:
        return self.s3.generate_presigned_url(method, Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=expires_in)

