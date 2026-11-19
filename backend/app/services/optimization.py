from typing import Any

import pandas as pd


def menu_recommendations(frame: pd.DataFrame) -> dict[str, Any]:
    products = frame.groupby(
        ["product_id", "product_detail", "product_category"], as_index=False
    ).agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"), average_price=("unit_price", "mean"))
    total_revenue = float(products["revenue"].sum())
    products["revenue_share"] = products["revenue"] / total_revenue
    revenue_median = float(products["revenue"].median())
    quantity_median = float(products["quantity"].median())

    recommendations = []
    for _, row in products.iterrows():
        if row["revenue"] >= revenue_median and row["quantity"] >= quantity_median:
            title = "Promote as a strong core product"
            action = "Use in high-visibility placements and monitor continued performance."
            evidence = "Above-median revenue and above-median units sold."
        elif row["revenue"] >= revenue_median:
            title = "Investigate as a premium opportunity"
            action = "Review placement and bundles; do not infer price elasticity."
            evidence = "Above-median revenue with relatively lower units sold."
        elif row["quantity"] >= quantity_median:
            title = "Investigate volume-to-revenue conversion"
            action = "Review basket placement, merchandising, and price/value perception."
            evidence = "Above-median units sold with below-median revenue."
        else:
            title = "Investigate before changing the menu"
            action = "Review category context, seasonality, and operational constraints."
            evidence = "Below-median revenue and below-median units sold."
        recommendations.append({
            "title": title,
            "business_issue": evidence,
            "supporting_metrics": {
                "revenue": round(float(row["revenue"]), 2),
                "quantity": int(row["quantity"]),
                "revenue_share": round(float(row["revenue_share"]), 6),
                "average_price": round(float(row["average_price"]), 2),
            },
            "recommended_action": action,
            "expected_direction": "Investigate or promote; no guaranteed financial impact",
            "confidence": "Moderate",
            "methodology": "Median revenue and median units sold, not a causal model.",
        })
    recommendations.sort(key=lambda row: (row["supporting_metrics"]["revenue"], row["supporting_metrics"]["quantity"]), reverse=True)
    return {
        "thresholds": {"revenue_median": round(revenue_median, 2), "quantity_median": round(quantity_median, 2)},
        "recommendations": recommendations,
        "limitation": "Low observed sales alone is not sufficient to recommend removal.",
    }


def pricing_scenario(frame: pd.DataFrame, product_detail: str, price_change_percent: float, quantity_assumption: str = "baseline") -> dict[str, Any]:
    products = frame[frame["product_detail"] == product_detail]
    if products.empty:
        raise ValueError("Product not found.")
    current_price = float(products["unit_price"].mean())
    baseline_quantity = int(products["transaction_qty"].sum())
    assumptions = {
        "baseline": baseline_quantity,
        "conservative": round(baseline_quantity * 0.98),
        "moderate": round(baseline_quantity * 1.00),
        "aggressive": round(baseline_quantity * 1.02),
    }
    simulated_quantity = assumptions.get(quantity_assumption, baseline_quantity)
    simulated_price = current_price * (1 + price_change_percent / 100)
    baseline_revenue = current_price * baseline_quantity
    simulated_revenue = simulated_price * simulated_quantity
    return {
        "product_detail": product_detail,
        "current_unit_price": round(current_price, 2),
        "price_change_percent": price_change_percent,
        "simulated_unit_price": round(simulated_price, 2),
        "quantity_assumption": quantity_assumption,
        "simulated_quantity": simulated_quantity,
        "baseline_revenue": round(baseline_revenue, 2),
        "simulated_revenue": round(simulated_revenue, 2),
        "revenue_difference": round(simulated_revenue - baseline_revenue, 2),
        "percentage_difference": round(((simulated_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue else 0, 2),
        "warning": "Hypothetical scenario only. No actual price elasticity or causal demand response is assumed.",
    }
