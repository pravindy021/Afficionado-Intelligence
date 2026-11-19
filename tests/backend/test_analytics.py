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


def test_api_analytics_endpoints_return_real_schema():
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


def test_phase4_api_routes():
    client = TestClient(app)
    for path in ["segmentation", "clustering", "anomalies", "statistics"]:
        response = client.get(f"/api/analytics/{path}")
        assert response.status_code == 200


def test_forecast_suitability_is_explicitly_unsupported():
    client = TestClient(app)
    response = client.get("/api/forecast/suitability")
    assert response.status_code == 200
    assert response.json()["supported"] is False
    assert "calendar date" in response.json()["reason"].lower()


def test_menu_and_pricing_endpoints_are_grounded():
    client = TestClient(app)
    menu = client.get("/api/optimization/menu")
    products = client.get("/api/analytics/products")
    assert menu.status_code == 200
    assert menu.json()["limitation"]
    product_name = products.json()["products"][0]["product_detail"]
    scenario = client.get(
        "/api/optimization/pricing",
        params={"product_detail": product_name, "price_change_percent": 10, "quantity_assumption": "baseline"},
    )
    assert scenario.status_code == 200
    assert "hypothetical" in scenario.json()["warning"].lower()


def test_copilot_returns_grounded_response():
    client = TestClient(app)
    response = client.post("/api/copilot", json={"question": "Which product generates the most revenue?"})
    assert response.status_code == 200
    assert "evidence" in response.json()
