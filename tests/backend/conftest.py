import pandas as pd
import pytest

from app.api import data as data_api
from app.core import data_store


@pytest.fixture(autouse=True)
def synthetic_dataset(tmp_path, monkeypatch):
    products = [
        ("Ethiopia Single Origin", "Coffee", "Whole Bean", 18.00, 8),
        ("House Espresso", "Coffee", "Espresso", 3.50, 10),
        ("Vanilla Latte", "Coffee", "Latte", 5.50, 9),
        ("Cold Brew", "Coffee", "Cold Brew", 4.75, 8),
        ("Matcha Latte", "Tea", "Tea Latte", 6.00, 6),
        ("Earl Grey", "Tea", "Brewed Tea", 3.25, 4),
        ("Chai Latte", "Tea", "Tea Latte", 5.25, 7),
        ("Almond Croissant", "Bakery", "Pastry", 4.50, 6),
        ("Blueberry Muffin", "Bakery", "Muffin", 3.75, 5),
        ("Avocado Toast", "Food", "Toast", 10.50, 4),
        ("Granola Bowl", "Food", "Breakfast", 8.50, 5),
        ("Seasonal Pour Over", "Coffee", "Brewed", 7.00, 7),
    ]
    locations = [("Astoria", 1), ("Manhattan", 2), ("Brooklyn", 3)]
    rows = []
    transaction_id = 1
    for product_id, (detail, category, product_type, price, quantity) in enumerate(products, start=1):
        for occurrence, sold in enumerate((quantity // 2, quantity - quantity // 2)):
            location, store_id = locations[(product_id + occurrence) % len(locations)]
            hour = 7 + ((product_id + occurrence * 5) % 12)
            rows.append(
                {
                    "transaction_id": transaction_id,
                    "year": 2025,
                    "transaction_time": f"{hour:02d}:00:00",
                    "transaction_qty": sold,
                    "store_id": store_id,
                    "store_location": location,
                    "product_id": product_id,
                    "unit_price": price,
                    "product_category": category,
                    "product_type": product_type,
                    "product_detail": detail,
                }
            )
            transaction_id += 1

    frame = pd.DataFrame(rows, columns=data_store.EXPECTED_COLUMNS)
    dataset_path = tmp_path / "synthetic_transactions.xlsx"
    processed_dir = tmp_path / "processed"
    frame.to_excel(dataset_path, index=False)

    monkeypatch.setattr(data_store, "DATASET_PATH", dataset_path)
    monkeypatch.setattr(data_store, "PROCESSED_DIR", processed_dir)
    monkeypatch.setattr(data_store, "VERSION_PATH", processed_dir / "dataset_version.json")
    monkeypatch.setattr(data_api, "DATASET_PATH", dataset_path)
    monkeypatch.setattr(data_api, "VERSION_PATH", processed_dir / "dataset_version.json")
    data_store.load_transactions.cache_clear()
    try:
        yield frame
    finally:
        data_store.load_transactions.cache_clear()
