# Architecture

## Application layers

- React/Vite presentation layer
- FastAPI REST API
- Pandas analytics services
- SQLite/PostgreSQL-ready persistence direction
- Excel source data under `data/raw`

## Data layers

The source workbook is never modified. Raw source copies live under `data/raw`; validated and
processed derivatives are generated only when needed under `data/`.

## API

- `GET /api/health`
- `GET /api/analytics/executive`
- `GET /api/analytics/products`
- `GET /api/analytics/categories`
- `GET /api/analytics/stores`
- `GET /api/analytics/revenue`
- `GET /api/data/profile`

The product endpoint accepts `search`, `category`, and `product_type` query parameters.
