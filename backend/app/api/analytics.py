from fastapi import APIRouter, Query

from app.core.data_store import load_transactions
from app.services.analytics import (
    executive_summary,
    filter_products,
    revenue_intelligence,
    category_analytics,
    store_analytics,
)
from app.services.advanced_analytics import (
    anomaly_detection,
    product_clustering,
    product_segments,
    statistical_intelligence,
)

router = APIRouter(tags=["analytics"])


@router.get("/analytics/executive")
def executive():
    return executive_summary(load_transactions())


@router.get("/analytics/products")
def products(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    product_type: str | None = Query(default=None),
):
    return {
        "products": filter_products(
            load_transactions(),
            search=search,
            category=category,
            product_type=product_type,
        )
    }


@router.get("/analytics/categories")
def categories():
    return {"categories": category_analytics(load_transactions())}


@router.get("/analytics/stores")
def stores():
    return {"stores": store_analytics(load_transactions())}


@router.get("/analytics/revenue")
def revenue():
    return revenue_intelligence(load_transactions())


@router.get("/analytics/segmentation")
def segmentation(revenue_threshold: float = Query(default=0.5, ge=0.1, le=2.0),
                 quantity_threshold: float = Query(default=0.5, ge=0.1, le=2.0)):
    return product_segments(load_transactions(), revenue_threshold, quantity_threshold)


@router.get("/analytics/clustering")
def clustering(clusters: int = Query(default=3, ge=2, le=6)):
    return product_clustering(load_transactions(), clusters)


@router.get("/analytics/anomalies")
def anomalies():
    return anomaly_detection(load_transactions())


@router.get("/analytics/statistics")
def statistics():
    return statistical_intelligence(load_transactions())
