from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Any


@dataclass(frozen=True)
class S3ObjectRef:
    bucket: str
    key: str


def validate_csv_key(key: str) -> None:
    """
    Simple validation rule:
    - must end with .csv
    - must not contain path traversal
    """
    if not key.lower().endswith(".csv"):
        raise ValueError("Only .csv files are supported")
    if ".." in key.replace("\\", "/").split("/"):
        raise ValueError("Invalid key path traversal detected")


def list_candidate_objects(objects: Iterable[Dict[str, Any]]) -> list[S3ObjectRef]:
    """
    Convert a list of dicts (like S3 list_objects output) into S3ObjectRef items.
    Expected dicts contain: Bucket, Key
    """
    results: list[S3ObjectRef] = []
    for obj in objects:
        bucket = obj["Bucket"]
        key = obj["Key"]
        validate_csv_key(key)
        results.append(S3ObjectRef(bucket=bucket, key=key))
    return results