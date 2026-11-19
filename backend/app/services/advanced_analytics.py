from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def product_segments(frame: pd.DataFrame, revenue_threshold: float = 0.5, quantity_threshold: float = 0.5) -> dict[str, Any]:
    products = frame.groupby(
        ["product_id", "product_detail", "product_category", "product_type"], as_index=False
    ).agg(
        revenue=("revenue", "sum"),
        quantity=("transaction_qty", "sum"),
        average_price=("unit_price", "mean"),
    )
    total_revenue = float(products["revenue"].sum())
    total_quantity = float(products["quantity"].sum())
    products["revenue_share"] = products["revenue"] / total_revenue
    products["quantity_share"] = products["quantity"] / total_quantity
    revenue_median = float(products["revenue"].median())
    quantity_median = float(products["quantity"].median())
    price_median = float(products["average_price"].median())

    def classify(row: pd.Series) -> tuple[str, str]:
        high_revenue = row["revenue"] >= revenue_median * (1 + revenue_threshold - 0.5)
        high_quantity = row["quantity"] >= quantity_median * (1 + quantity_threshold - 0.5)
        if high_revenue and high_quantity:
            return "Stars", "Above-median revenue and above-median units sold."
        if high_revenue and row["average_price"] >= price_median:
            return "Premium Performers", "Above-median revenue with an above-median average unit price."
        if high_revenue:
            return "Hidden Gems", "Above-median revenue with relatively lower units or average price."
        if high_quantity:
            return "Volume Drivers", "Above-median units sold with below-median revenue."
        return "Underperformers", "Below-median revenue and below-median units sold."

    classified = products.apply(
        lambda row: pd.Series(classify(row), index=["segment", "reason"]),
        axis=1,
    )
    products = pd.concat([products, classified], axis=1)
    summary = products.groupby("segment", as_index=False).agg(
        products=("product_id", "count"),
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
    )
    return {
        "thresholds": {
            "revenue_median": round(revenue_median, 2),
            "quantity_median": round(quantity_median, 2),
            "average_price_median": round(price_median, 2),
            "revenue_threshold": revenue_threshold,
            "quantity_threshold": quantity_threshold,
        },
        "summary": summary.sort_values("revenue", ascending=False).to_dict(orient="records"),
        "products": products.sort_values("revenue", ascending=False).to_dict(orient="records"),
    }


def product_clustering(frame: pd.DataFrame, clusters: int = 3) -> dict[str, Any]:
    products = frame.groupby(
        ["product_id", "product_detail", "product_category"], as_index=False
    ).agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"), average_price=("unit_price", "mean"))
    if len(products) < 4:
        return {"supported": False, "reason": "Fewer than four products are available.", "points": [], "elbow": []}

    features = ["revenue", "quantity", "average_price"]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(products[features])
    cluster_count = max(2, min(int(clusters), min(6, len(products) - 1)))

    elbow = []
    silhouette_values = []
    for count in range(2, min(7, len(products))):
        model = KMeans(n_clusters=count, random_state=42, n_init=20)
        labels = model.fit_predict(scaled)
        elbow.append({"clusters": count, "inertia": round(float(model.inertia_), 2)})
        silhouette_values.append({"clusters": count, "silhouette": round(float(silhouette_score(scaled, labels)), 4)})

    model = KMeans(n_clusters=cluster_count, random_state=42, n_init=20)
    labels = model.fit_predict(scaled)
    pca = PCA(n_components=2, random_state=42)
    coordinates = pca.fit_transform(scaled)
    products["cluster"] = labels
    products["pca_x"] = coordinates[:, 0]
    products["pca_y"] = coordinates[:, 1]

    interpretations = []
    for cluster_id in sorted(products["cluster"].unique()):
        subset = products[products["cluster"] == cluster_id]
        interpretations.append({
            "cluster": int(cluster_id),
            "product_count": int(len(subset)),
            "average_revenue": round(float(subset["revenue"].mean()), 2),
            "average_quantity": round(float(subset["quantity"].mean()), 2),
            "average_price": round(float(subset["average_price"].mean()), 2),
        })
    return {
        "supported": True,
        "cluster_count": cluster_count,
        "silhouette_score": round(float(silhouette_score(scaled, labels)), 4),
        "elbow": elbow,
        "silhouette_values": silhouette_values,
        "explained_variance": round(float(pca.explained_variance_ratio_.sum()), 4),
        "clusters": interpretations,
        "points": products[
            ["product_detail", "revenue", "quantity", "average_price", "cluster", "pca_x", "pca_y"]
        ].to_dict(orient="records"),
    }


def anomaly_detection(frame: pd.DataFrame) -> dict[str, Any]:
    products = frame.groupby(
        ["product_id", "product_detail", "product_category"], as_index=False
    ).agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"))
    anomalies = []

    def iqr_flags(series: pd.Series) -> pd.Series:
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return (series < lower) | (series > upper)

    for field in ["revenue", "quantity"]:
        zscores = (products[field] - products[field].mean()) / products[field].std(ddof=0)
        for _, row in products.iterrows():
            iqr = bool(iqr_flags(products[field]).loc[row.name])
            z = float(abs(zscores.loc[row.name]))
            if iqr or z >= 3:
                anomalies.append({
                    "product_detail": row["product_detail"],
                    "category": row["product_category"],
                    "field": field,
                    "value": round(float(row[field]), 2),
                    "absolute_zscore": round(z, 3),
                    "method": "IQR" if iqr else "Z-score",
                    "severity": "High" if z >= 3 else "Moderate",
                })

    store = frame.groupby("store_location", as_index=False).agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"))
    for field in ["revenue", "quantity"]:
        flags = iqr_flags(store[field])
        for _, row in store[flags].iterrows():
            anomalies.append({
                "product_detail": row["store_location"],
                "category": "Store",
                "field": field,
                "value": round(float(row[field]), 2),
                "absolute_zscore": None,
                "method": "IQR",
                "severity": "Moderate",
            })

    isolation_supported = len(products) >= 10
    isolation_count = 0
    if isolation_supported:
        scaler = StandardScaler()
        scaled = scaler.fit_transform(products[["revenue", "quantity"]])
        model = IsolationForest(contamination="auto", random_state=42)
        predictions = model.fit_predict(scaled)
        isolation_count = int((predictions == -1).sum())

    return {
        "methodology": {
            "iqr": "Outside Q1 - 1.5*IQR or Q3 + 1.5*IQR.",
            "z_score": "Absolute z-score of 3 or higher.",
            "isolation_forest": "Applied only when at least 10 products are available.",
        },
        "anomalies": sorted(anomalies, key=lambda row: row["severity"] != "High"),
        "isolation_forest": {"supported": isolation_supported, "outlier_count": isolation_count},
        "warning": "These are statistical anomalies, not evidence of fraud or operational failure.",
    }


def statistical_intelligence(frame: pd.DataFrame) -> dict[str, Any]:
    products = frame.groupby(
        ["product_id", "product_detail", "product_category"], as_index=False
    ).agg(revenue=("revenue", "sum"), quantity=("transaction_qty", "sum"), average_price=("unit_price", "mean"))
    numeric = products[["revenue", "quantity", "average_price"]]
    correlation = numeric.corr().where(pd.notna(numeric.corr()), 0)
    return {
        "descriptive_statistics": numeric.describe().transpose().reset_index().rename(columns={"index": "metric"}).to_dict(orient="records"),
        "correlation_matrix": [
            {"metric": column, **{row: round(float(correlation.loc[column, row]), 4) for row in correlation.columns}}
            for column in correlation.columns
        ],
        "outliers": {
            "revenue": int(((numeric["revenue"] - numeric["revenue"].mean()).abs() > 3 * numeric["revenue"].std(ddof=0)).sum()),
            "quantity": int(((numeric["quantity"] - numeric["quantity"].mean()).abs() > 3 * numeric["quantity"].std(ddof=0)).sum()),
            "average_price": int(((numeric["average_price"] - numeric["average_price"].mean()).abs() > 3 * numeric["average_price"].std(ddof=0)).sum()),
        },
        "limitations": ["Descriptive correlations do not imply causality.", "Only product-aggregate data is used."],
    }
