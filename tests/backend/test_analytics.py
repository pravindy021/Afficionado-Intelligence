import pandas as pd

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.analytics import (
    category_analytics,
    core_metrics,
    executive_summary,
    pareto_analysis,
    product_ranking,
)
from app.services.advanced_analytics import (
    anomaly_detection,
    product_clustering,
    product_segments,
    statistical_intelligence,
)


def sample_frame():
    return pd.DataFrame([
        {"transaction_id": 1, "year": 2025, "transaction_time": "07:00:00", "transaction_qty": 2, "unit_price": 3.0, "product_id": 1, "product_detail": "A", "product_category": "Coffee", "product_type": "Brewed", "revenue": 6.0, "store_location": "Astoria"},
        {"transaction_id": 2, "year": 2025, "transaction_time": "08:00:00", "transaction_qty": 1, "unit_price": 5.0, "product_id": 2, "product_detail": "B", "product_category": "Tea", "product_type": "Brewed Tea", "revenue": 5.0, "store_location": "Astoria"},
    ])


def test_executive_summary_uses_calculated_revenue():
    result = executive_summary(sample_frame())
    assert result["kpis"]["total_revenue"] == 11.0
    assert result["kpis"]["total_transactions"] == 2


def test_product_ranking_returns_expected_segment():
    result = product_ranking(sample_frame())
    assert len(result) == 2
    assert {row["segment"] for row in result}


def test_core_metrics_calculate_quantity_and_transaction_count():
    result = core_metrics(sample_frame())
    assert result["total_revenue"] == 11.0
    assert result["total_quantity"] == 3
    assert result["transaction_count"] == 2
    assert result["average_selling_price"] == 4.0


def test_category_aggregation_and_revenue_shares():
    result = category_analytics(sample_frame())
    coffee = next(row for row in result if row["product_category"] == "Coffee")
    tea = next(row for row in result if row["product_category"] == "Tea")
    assert coffee["revenue"] == 6.0
    assert tea["quantity"] == 1
    assert round(coffee["revenue_share"] + tea["revenue_share"], 8) == 1.0


def test_pareto_calculates_cumulative_share_and_abc_classes():
    result = pareto_analysis(sample_frame())
    assert result[0]["revenue"] == 6.0
    assert round(result[-1]["cumulative_revenue_share"], 8) == 1.0
    assert {row["abc_class"] for row in result} <= {"A", "B", "C"}


def test_invalid_data_is_rejected():
    frame = sample_frame()
    frame.loc[0, "transaction_qty"] = 0
    with pytest.raises(ValueError, match="positive"):
        core_metrics(frame)


def test_api_analytics_endpoints_return_real_schema(synthetic_dataset):
    client = TestClient(app)
    health = client.get("/api/health")
    executive = client.get("/api/analytics/executive")
    revenue = client.get("/api/analytics/revenue")
    products = client.get("/api/analytics/products", params={"search": "Ethiopia"})
    assert health.status_code == 200
    assert executive.status_code == 200
    assert revenue.status_code == 200
    assert products.status_code == 200
    assert "pareto" in revenue.json()
    expected_revenue = float(
        (synthetic_dataset["transaction_qty"] * synthetic_dataset["unit_price"]).sum()
    )
    assert executive.json()["kpis"]["total_revenue"] == expected_revenue
    assert executive.json()["kpis"]["total_transactions"] == len(synthetic_dataset)
    assert executive.json()["kpis"]["active_products"] == synthetic_dataset["product_id"].nunique()
    assert len(products.json()["products"]) == 1
    assert products.json()["products"][0]["product_detail"] == "Ethiopia Single Origin"


def test_data_profile_uses_temporary_excel_source(synthetic_dataset):
    response = TestClient(app).get("/api/data/profile")

    assert response.status_code == 200
    profile = response.json()
    assert profile["dataset"]["name"] == "synthetic_transactions.xlsx"
    assert profile["dataset"]["rows"] == len(synthetic_dataset)
    assert profile["dataset"]["columns"] == [
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
    assert profile["dataset"]["missing_values"] == 0
    assert list(synthetic_dataset.columns) == profile["dataset"]["columns"]
    for column in ["transaction_id", "year", "transaction_qty", "store_id", "product_id", "unit_price"]:
        assert pd.api.types.is_numeric_dtype(synthetic_dataset[column])
    assert synthetic_dataset["transaction_time"].map(lambda value: isinstance(value, str)).all()
    assert synthetic_dataset["store_location"].map(lambda value: isinstance(value, str)).all()


def test_product_segmentation_returns_supported_segments():
    result = product_segments(sample_frame())
    assert set(row["segment"] for row in result["summary"]) <= {
        "Stars", "Hidden Gems", "Volume Drivers", "Premium Performers", "Underperformers"
    }
    assert len(result["products"]) == 2


def test_product_clustering_handles_real_aggregate_data():
    frame = sample_frame()
    for index in range(3, 12):
        frame = pd.concat([frame, pd.DataFrame([{
            "transaction_id": index,
            "year": 2025,
            "transaction_time": "09:00:00",
            "transaction_qty": index,
            "unit_price": float(index),
            "product_id": index,
            "product_detail": f"P{index}",
            "product_category": "Coffee",
            "product_type": "Test",
            "revenue": float(index * index),
            "store_location": "Astoria",
        }])], ignore_index=True)
    result = product_clustering(frame, 3)
    assert result["supported"] is True
    assert len(result["points"]) >= 10


def test_anomaly_and_statistics_are_explainable():
    anomaly = anomaly_detection(sample_frame())
    statistics = statistical_intelligence(sample_frame())
    assert "methodology" in anomaly
    assert "fraud" in anomaly["warning"]
    assert "correlation_matrix" in statistics


def test_phase4_api_routes(synthetic_dataset):
    client = TestClient(app)
    segmentation = client.get("/api/analytics/segmentation")
    clustering = client.get("/api/analytics/clustering")
    anomalies = client.get("/api/analytics/anomalies")
    statistics = client.get("/api/analytics/statistics")

    assert segmentation.status_code == 200
    assert len(segmentation.json()["products"]) == synthetic_dataset["product_id"].nunique()
    assert clustering.status_code == 200
    assert clustering.json()["supported"] is True
    assert len(clustering.json()["points"]) == synthetic_dataset["product_id"].nunique()
    assert anomalies.status_code == 200
    assert "methodology" in anomalies.json()
    assert anomalies.json()["isolation_forest"]["supported"] is True
    assert "fraud" in anomalies.json()["warning"]
    assert statistics.status_code == 200
    assert {row["metric"] for row in statistics.json()["descriptive_statistics"]} == {
        "revenue",
        "quantity",
        "average_price",
    }
    assert len(statistics.json()["correlation_matrix"]) == 3


def test_forecast_suitability_is_explicitly_unsupported(synthetic_dataset):
    client = TestClient(app)
    response = client.get("/api/forecast/suitability")
    assert response.status_code == 200
    assert response.json()["supported"] is False
    assert "calendar date" in response.json()["reason"].lower()
    assert response.json()["available_history"]["year_values"] == [2025]


def test_menu_and_pricing_endpoints_are_grounded(synthetic_dataset):
    client = TestClient(app)
    menu = client.get("/api/optimization/menu")
    products = client.get("/api/analytics/products")
    assert menu.status_code == 200
    assert menu.json()["limitation"]
    assert len(menu.json()["recommendations"]) == synthetic_dataset["product_id"].nunique()
    expected_products = synthetic_dataset.assign(
        revenue=synthetic_dataset["transaction_qty"] * synthetic_dataset["unit_price"]
    ).groupby("product_detail", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("transaction_qty", "sum"),
        average_price=("unit_price", "mean"),
    )
    expected_top = expected_products.sort_values("revenue", ascending=False).iloc[0]
    product_name = products.json()["products"][0]["product_detail"]
    assert product_name == expected_top["product_detail"]
    assert menu.json()["recommendations"][0]["supporting_metrics"]["revenue"] == expected_top["revenue"]
    scenario = client.get(
        "/api/optimization/pricing",
        params={"product_detail": product_name, "price_change_percent": 10, "quantity_assumption": "baseline"},
    )
    assert scenario.status_code == 200
    assert "hypothetical" in scenario.json()["warning"].lower()
    assert scenario.json()["product_detail"] == product_name
    assert scenario.json()["simulated_unit_price"] > scenario.json()["current_unit_price"]
    assert scenario.json()["current_unit_price"] == expected_top["average_price"]


def test_copilot_returns_grounded_response(synthetic_dataset):
    client = TestClient(app)
    response = client.post("/api/copilot", json={"question": "Which product generates the most revenue?"})
    assert response.status_code == 200
    result = response.json()
    product_revenue = synthetic_dataset.assign(
        revenue=synthetic_dataset["transaction_qty"] * synthetic_dataset["unit_price"]
    ).groupby("product_detail")["revenue"].sum()
    expected_top = product_revenue.idxmax()
    assert result["evidence"][0]["metric"] == "product_revenue"
    assert result["evidence"][0]["product"] == expected_top
    assert result["evidence"][0]["value"] == product_revenue[expected_top]
