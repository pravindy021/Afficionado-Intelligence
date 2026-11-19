# Afficionado Intelligence — Future Evolution Progress

## Current State

This repository is in gap-analysis mode for future evolution. No features from the future roadmap
have been implemented in this pass.

## Gap Analysis Complete

The actual repository was inspected for:

- Backend entry point and API routes.
- Current analytics and Copilot services.
- SQLAlchemy persistence model declarations.
- Frontend routes and package dependencies.
- Dataset and processed-data connection.
- Security documentation and implementation.
- Docker and CI configuration.
- Existing tests and build configuration.

## Current Verified Capabilities

- Reusable core BI calculations.
- Product, category, store, revenue, Pareto, and ABC analytics.
- Product segmentation and clustering.
- IQR, Z-score, and Isolation Forest anomaly analysis.
- Descriptive and correlation analytics.
- Explicit forecast-unsuitability assessment.
- Hypothetical pricing scenario arithmetic.
- Menu investigation and structured recommendation data.
- Grounded deterministic Copilot response with evidence.
- Data profiling and dataset version JSON.
- Public landing page and responsive React shell.

## Current Verified Missing Capabilities

- Active database migration configuration.
- Active authentication and RBAC.
- Tenant/workspace isolation.
- Persistent audit and conversation storage.
- Real agent registry and tool-permission enforcement.
- External consequential-action approvals.
- Persistent datasets, forecast runs, recommendations, and model evaluations.
- Schema-change and data-freshness monitoring.
- Scheduled or on-demand reports.
- Real forecast model execution.
- Graph database or graph projection.

## Next Implementation Task

Implement Phase F1: security and persistence foundation.

Before this work begins, create the next implementation slice with:

1. An Alembic baseline and database session.
2. A focused SQLite developer database configuration.
3. User and role models.
4. Password hashing and login.
5. Protected analytics routes.
6. Workspace/tenant ownership and isolation tests.

Do not claim multi-tenancy until tenant isolation is implemented and tested.

## Verification State

- Existing backend tests: 14 passing.
- Existing frontend production build: passing.
- Docker CLI: unavailable in the current audit environment.
- Source forecast: unsupported due to no calendar dates.
- Dataset basket analysis: unsupported due to one row per transaction ID.
- Profit analysis: unsupported due to missing cost and expense fields.
