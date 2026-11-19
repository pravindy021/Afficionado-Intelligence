from pathlib import Path
from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = ROOT / "data" / "Afficionado Coffee Roasters.xlsx"
RAW_DATASET_PATH = ROOT / "data" / "raw" / "Afficionado Coffee Roasters.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
VERSION_PATH = PROCESSED_DIR / "dataset_version.json"
EXPECTED_COLUMNS = [
    "transaction_id",
    "year",
    "transaction_time",
    "transaction_qty",
    "store_id",
    "store_location",
    "product_id",
    "unit_price",
    "product_category",
    "product_type",
    "product_detail",
]

NUMERIC_COLUMNS = ["transaction_qty", "unit_price", "transaction_id", "year", "store_id", "product_id"]


def validate_transactions(frame: pd.DataFrame) -> dict:
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    if frame.empty:
        raise ValueError("The source dataset contains no rows.")

    invalid_types = []
    for column in NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(frame[column]):
            invalid_types.append(column)
    if invalid_types:
        raise ValueError(f"Columns must be numeric: {', '.join(invalid_types)}")

    missing = frame[EXPECTED_COLUMNS].isna().sum()
    invalid = {
        "missing_by_column": {key: int(value) for key, value in missing.items() if value},
        "duplicate_rows": int(frame.duplicated().sum()),
        "nonpositive_quantity": int((frame["transaction_qty"] <= 0).sum()),
        "nonpositive_unit_price": int((frame["unit_price"] <= 0).sum()),
    }
    return invalid


def run_ingestion_pipeline() -> dict:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    raw = pd.read_excel(DATASET_PATH)
    quality = validate_transactions(raw)
    if quality["missing_by_column"]:
        raise ValueError("Cannot process rows with missing required values.")
    if quality["nonpositive_quantity"] or quality["nonpositive_unit_price"]:
        raise ValueError("Quantity and unit price must be positive.")

    frame = raw[EXPECTED_COLUMNS].copy()
    frame["revenue"] = frame["transaction_qty"] * frame["unit_price"]
    frame["hour"] = frame["transaction_time"].astype(str).str.slice(0, 2).astype(int)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(DATASET_PATH.read_bytes()).hexdigest()
    processed_path = PROCESSED_DIR / "transactions_processed.csv"
    frame.to_csv(processed_path, index=False)
    version = {
        "version": "v1",
        "source_name": DATASET_PATH.name,
        "source_sha256": source_hash,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "row_count": int(len(frame)),
        "revenue_formula": "transaction_qty * unit_price",
        "basket_analysis_supported": False,
        "profit_analysis_supported": False,
        "quality": quality,
    }
    VERSION_PATH.write_text(json.dumps(version, indent=2), encoding="utf-8")
    return version


@lru_cache(maxsize=1)
def load_transactions() -> pd.DataFrame:
    run_ingestion_pipeline()
    frame = pd.read_csv(PROCESSED_DIR / "transactions_processed.csv")
    return frame
