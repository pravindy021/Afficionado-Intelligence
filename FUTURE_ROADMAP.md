# Afficionado Intelligence — Future Evolution Roadmap

## Gap Analysis Basis

This roadmap reflects the current repository. It is not a claim that features exist simply because
documentation or class names mention them.

## Capability Classification

| Future capability | Status | Evidence and next decision |
|---|---|---|
| Agentic business intelligence | Partial / missing execution | A deterministic grounded Copilot exists in `backend/app/services/copilot.py`, but it has no specialized agents, tool registry, tool permissions, timeout policy, approval workflow, or agent audit trail. |
| Prescriptive analytics | Partially implemented | Menu recommendations and hypothetical pricing exist, but evidence is mostly median-based and recommendations are not persisted or configurable. |
| Advanced simulation | Partially implemented | One-product hypothetical price/quantity scenarios exist. Product-mix, demand, promotion, and multi-scenario comparisons are missing. |
| Real-time monitoring | Missing | No refresh watcher, event queue, notification system, model degradation monitor, or periodic task is implemented. |
| Natural language analytics | Partially implemented | Copilot has keyword intent detection and real analytics evidence, but no general intent planner, tool allowlist registry, query validation layer, or secure result citation model. |
| Data governance | Partially implemented | Raw/processed layers, hash metadata, quality checks, data dictionary, and source profiling exist. Lineage history, schema-change detection, freshness alerts, and governance audit storage are missing. |
| MLOps | Missing / partially modeled | SQLAlchemy model classes exist, but no active registry, experiment store, model evaluation history, drift calculation, approval workflow, or retraining process is connected. |
| Business knowledge graph | Missing | Relational models exist, but no graph projection or graph query model is implemented. A graph database is not justified yet. |
| Enterprise SaaS | Missing | Docker and CORS exist, but there is no authentication, password hashing, RBAC, users, workspaces, tenant isolation, usage limits, migration setup, or active audit storage. |
| Advanced reporting | Missing | No report-generation endpoints or scheduled/on-demand report workflow exists. |

## Dataset Constraints

- 149,116 source rows.
- 2025-only coverage.
- `transaction_time` exists, but no calendar date.
- `transaction_id` is unique per source row, so basket analysis is unsupported.
- No cost or expense fields exist, so revenue is not profit and profitability is unsupported.
- No real-time refresh source exists.

## Prioritized Incremental Plan

### Phase F1 — Security and persistence foundation
1. Add an active SQLite database session and migration baseline.
2. Add users, roles, workspaces, and tenant ownership fields.
3. Add password hashing and login/session or token authentication.
4. Add protected API routes and RBAC.
5. Add tenant-scoped queries and integration tests.

### Phase F2 — Governance and audit foundation
1. Persist dataset versions and quality scores.
2. Detect schema and data-quality changes between ingestion runs.
3. Track lineage from source workbook to processed CSV.
4. Add freshness indicators and audit events.
5. Expose governance history through read-only APIs.

### Phase F3 — Controlled agent tools
1. Introduce explicit tool definitions for existing analytics functions.
2. Add agent names, input schemas, permissions, timeouts, and audit records.
3. Route Copilot intent through a restricted tool planner.
4. Add human approval metadata for any consequential operation.
5. Keep external actions disabled until identity and approval are implemented.

### Phase F4 — Prescriptive analytics and simulation
1. Add configurable thresholds and constraints to recommendations.
2. Persist structured recommendation evidence.
3. Add product-mix and demand-assumption scenarios.
4. Return clear historical baseline, assumptions, outputs, uncertainty, and limitations.
5. Preserve the rule that simulated values are never causal estimates.

### Phase F5 — Grounded natural-language analytics
1. Replace keyword-only routing with classified intent and entity extraction.
2. Add explicit metric-tool allowlisting.
3. Validate parameters before analytics execution.
4. Add evidence citations and missing-information responses.
5. Never permit arbitrary SQL from model output.

### Phase F6 — Reporting
1. Add on-demand executive, product, revenue, anomaly, and recommendation reports.
2. Include dataset version, calculation period, methodology, and limitations.
3. Prefer CSV and HTML/PDF export over scheduled jobs in the first increment.
4. Add only actual report calculations.

### Phase F7 — Monitoring and MLOps
1. Add a model registry and evaluation records using the existing relational database.
2. Add dataset quality and schema-change monitoring.
3. Add anomaly trend and data freshness notifications.
4. Implement forecast-monitoring only if a defensible date series becomes available.
5. Add approval-gated retraining jobs only where meaningful.

### Phase F8 — SaaS hardening
1. Complete workspace-level navigation and tenant isolation tests.
2. Add API access scopes and usage limits.
3. Expand audit reporting.
4. Add operational health and readiness checks.

### Phase F9 — Knowledge graph
1. Defer a graph database.
2. Evaluate a graph projection only after tenants, governance, and stable recommendation IDs exist.
3. Prefer relational joins until graph query patterns provide clear value.

## Explicitly Not Supportable

- Complete-order basket analysis.
- Revenue-by-calendar-date forecasts.
- Profit and margin analysis.
- Causal price elasticity.
- Real-time monitoring.
- Customer-personalized analytics.
- Multi-tenancy claims before tenant-isolated implementation and tests.
