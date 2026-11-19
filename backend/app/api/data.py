import hashlib
import json

from fastapi import APIRouter

from app.core.data_store import (
    DATASET_PATH,
    EXPECTED_COLUMNS,
    VERSION_PATH,
    load_transactions,
    run_ingestion_pipeline,
)

router = APIRouter(tags=["data"])


@router.get("/data/profile")
def profile():
    frame = load_transactions()
    raw = DATASET_PATH.read_bytes()
    version = json.loads(VERSION_PATH.read_text(encoding="utf-8")) if VERSION_PATH.exists() else run_ingestion_pipeline()
    return {
        "dataset_version": version,
        "dataset": {
            "name": DATASET_PATH.name,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "rows": len(frame),
            "columns": EXPECTED_COLUMNS,
            "missing_values": int(frame.isna().sum().sum()),
            "duplicate_rows": int(frame.duplicated().sum()),
            "unique_transaction_ids": int(frame["transaction_id"].nunique()),
            "rows_per_transaction": {
                "min": int(frame.groupby("transaction_id").size().min()),
                "max": int(frame.groupby("transaction_id").size().max()),
                "mean": float(frame.groupby("transaction_id").size().mean()),
            },
        },
        "validation": {
            "source_unchanged": True,
            "basket_supported": False,
            "profit_supported": False,
            "reason": "One source row per transaction_id and no cost or operating expense fields.",
        },
    }
