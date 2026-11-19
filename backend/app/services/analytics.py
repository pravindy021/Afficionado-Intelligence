from typing import Any

import pandas as pd


def validate_analytics_frame(frame: pd.DataFrame) -> None:
    required = {"transaction_id", "transaction_qty", "unit_price", "revenue", "product_id", "product_detail", "product_category", "store_location"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Analytics frame missing columns: {', '.join(missing)}")
    if frame.empty:
        raise ValueError("Analytics frame contains no rows.")
    if (frame["transaction_qty"] <= 0).any() or (frame["unit_price"] <= 0).any():
        raise ValueError("Transaction quantities and unit prices must be positive.")


def core_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    validate_analytics_frame(frame)
    return {
        "total_revenue": round(float(frame["revenue"].sum()), 2),
        "total_quantity": int(frame["transaction_qty"].sum()),
        "transaction_count": int(frame["transaction_id"].nunique()),
        "average_selling_price": round(float(frame["unit_price"].mean()), 2),
        "average_transaction_value": round(
            float(frame.groupby("transaction_id", sort=False)["revenue"].sum().mean()), 2
        ),
    }


def category_analytics(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validate_analytics_frame(frame)
    total_revenue = float(frame["revenue"].sum())
    table = frame.groupby("product_category", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("transaction_qty", "sum"),
        transactions=("transaction_id", "nunique"),
    )
    table["revenue_share"] = table["revenue"] / total_revenue
    table["quantity_share"] = table["quantity"] / float(table["quantity"].sum())
    return table.sort_values("revenue", ascending=False).to_dict(orient="records")


def store_analytics(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validate_analytics_frame(frame)
    total_revenue = float(frame["revenue"].sum())
    table = frame.groupby("store_location", as_index=False).agg(
        revenue=("revenue", "sum"),
        quantity=("transaction_qty", "sum"),
        transactions=("transaction_id", "nunique"),
        active_products=("product_id", "nunique"),
    )
    table["revenue_share"] = table["revenue"] / total_revenue
    return table.sort_values("revenue", ascending=False).to_dict(orient="records")


def pareto_analysis(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validate_analytics_frame(frame)
    table = frame.groupby(["product_id", "product_detail"], as_index=False)["revenue"].sum()
    table = table.sort_values("revenue", ascending=False).reset_index(drop=True)
    total = float(table["revenue"].sum())
    table["revenue_share"] = table["revenue"] / total
    table["cumulative_revenue_share"] = table["revenue_share"].cumsum()
    table["abc_class"] = table["cumulative_revenue_share"].apply(
        lambda value: "A" if value <= 0.80 else "B" if value <= 0.95 else "C"
    )
    return table.to_dict(orient="records")


def executive_summary(frame: pd.DataFrame) -> dict[str, Any]:
    validate_analytics_frame(frame)
    metrics = core_metrics(frame)
    product_revenue = frame.groupby(
        ["product_id", "product_detail", "product_category"], as_index=False
    )["revenue"].sum()
    top_product = product_revenue.sort_values("revenue", ascending=False).iloc[0]
    category_revenue = frame.groupby("product_category", as_index=False)["revenue"].sum()
    top_category = category_revenue.sort_values("revenue", ascending=False).iloc[0]

    trend = (
        frame.assign(hour=frame["transaction_time"].astype(str).str.slice(0, 2).astype(int))
        .groupby("hour", as_index=False)
        .agg(revenue=("revenue", "sum"), transactions=("transaction_id", "nunique"))
        .sort_values("hour")
    )

    top_products = product_revenue.nlargest(10, "revenue")
    category_revenue["share"] = category_revenue["revenue"] / frame["revenue"].sum()
    store_revenue = frame.groupby("store_location", as_index=False).agg(
        revenue=("revenue", "sum"),
        transactions=("transaction_id", "nunique"),
        units=("transaction_qty", "sum"),
    )

    return {
        "kpis": {
            **metrics,
            "total_revenue": metrics["total_revenue"],
            "total_transactions": metrics["transaction_count"],
            "total_units": metrics["total_quantity"],
            "active_products": int(frame["product_id"].nunique()),
            "top_product": str(top_product["product_detail"]),
            "top_category": str(top_category["product_category"]),
        },
        "revenue_trend": trend.to_dict(orient="records"),
        "category_contribution": category_revenue.sort_values("revenue", ascending=False).to_dict(
            orient="records"
        ),
        "top_products": top_products.to_dict(orient="records"),
        "store_comparison": store_revenue.sort_values("revenue", ascending=False).to_dict(
            orient="records"
        ),
        "insights": [
            f"{top_product['product_detail']} is the highest-revenue product at "
            f"${top_product['revenue']:,.2f}.",
            f"{top_category['product_category']} is the largest revenue category.",
            "All transaction IDs represent one source line; market basket analysis is not supported.",
        ],
        "methodology": {
            "revenue": "transaction_qty * unit_price",
            "period": "Year 2025",
            "granularity": "Transaction-level source rows",
        },
    }


def product_ranking(frame: pd.DataFrame) -> list[dict[str, Any]]:
    validate_analytics_frame(frame)
    ranking = frame.groupby(
        ["product_id", "product_detail", "product_category", "product_type"], as_index=False
    ).agg(
        units=("transaction_qty", "sum"),
        revenue=("revenue", "sum"),
        transactions=("transaction_id", "nunique"),
        average_price=("unit_price", "mean"),
    )
    total_revenue = ranking["revenue"].sum()
    ranking["revenue_share"] = ranking["revenue"] / total_revenue
    ranking["median_units"] = ranking["units"].median()
    ranking["median_revenue"] = ranking["revenue"].median()
    ranking["segment"] = ranking.apply(
        lambda row: (
            "Star"
            if row["revenue"] >= row["median_revenue"]
            and row["units"] >= row["median_units"]
            else "Premium Performer"
            if row["revenue"] >= row["median_revenue"]
            else "Volume Driver"
            if row["units"] >= row["median_units"]
            else "Underperformer"
        ),
        axis=1,
    )
    return ranking.sort_values("revenue", ascending=False).to_dict(orient="records")


def filter_products(
    frame: pd.DataFrame,
    search: str | None = None,
    category: str | None = None,
    product_type: str | None = None,
) -> list[dict[str, Any]]:
    ranking = product_ranking(frame)
    products = pd.DataFrame(ranking)
    if search:
        needle = search.casefold()
        products = products[
            products["product_detail"].fillna("").astype(str).str.casefold().str.contains(needle, regex=False)
        ]
    if category:
        products = products[products["product_category"] == category]
    if product_type:
        products = products[products["product_type"] == product_type]
    return products.to_dict(orient="records")


def revenue_intelligence(frame: pd.DataFrame) -> dict[str, Any]:
    validate_analytics_frame(frame)
    pareto = pareto_analysis(frame)
    categories = category_analytics(frame)
    stores = store_analytics(frame)
    hourly = (
        frame.groupby("hour", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"))
        .sort_values("hour")
        if "hour" in frame.columns
        else pd.DataFrame(columns=["hour", "revenue", "quantity"])
    )
    ranked = sorted(pareto, key=lambda row: row["revenue"], reverse=True)
    top_revenue_share = sum(float(row["revenue_share"]) for row in ranked[:10])
    return {
        "metrics": core_metrics(frame),
        "category_comparison": categories,
        "store_comparison": stores,
        "pareto": pareto,
        "hourly_trend": hourly.to_dict(orient="records"),
        "concentration": {
            "top_10_product_revenue_share": round(top_revenue_share, 6),
            "top_product_revenue": ranked[0]["revenue"] if ranked else 0,
        },
        "top_products": ranked[:10],
        "bottom_products": ranked[-10:][::-1],
        "limitations": {
            "date_trend_supported": False,
            "reason": "The source contains year and transaction_time only, with no calendar date.",
            "hourly_trend_supported": True,
        },
    }
