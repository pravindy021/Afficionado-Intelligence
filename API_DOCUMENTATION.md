# API Documentation

Base URL: `http://localhost:8000/api`

## Core
- `GET /health`
- `GET /data/profile`

## Analytics
- `GET /analytics/executive`
- `GET /analytics/products?search=&category=&product_type=`
- `GET /analytics/categories`
- `GET /analytics/stores`
- `GET /analytics/revenue`
- `GET /analytics/segmentation?revenue_threshold=&quantity_threshold=`
- `GET /analytics/clustering?clusters=`
- `GET /analytics/anomalies`
- `GET /analytics/statistics`

## Predictive and Business
- `GET /forecast/suitability`
- `GET /optimization/menu`
- `GET /optimization/pricing?product_detail=&price_change_percent=&quantity_assumption=`
- `POST /copilot` with JSON `{"question":"..."}`.

All numerics are computed from the source workbook or explicitly labelled scenario/hypothesis values.
