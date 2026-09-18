# Phase roadmap

## Phase 1 — deployable core loop (implemented here)

1. PostgreSQL schema and migrations foundation.
2. API-Sports football fixture retrieval and cache.
3. Explicit provider status (`live`, `cached`, `stale`, `unavailable`) and structured logs.
4. Rule-based Match Winner and Over/Under Goals predictions.
5. Persisted predictions with engine/version and input provenance.
6. Health endpoint and minimal React read-only screen.
7. Tests for prediction logic and provider failure behavior.
8. Render and container configuration.

## Phase 2 — product foundation

- authentication and account lifecycle;
- competition/team/fixture search and pagination;
- Double Chance and Both Teams to Score;
- historical results and prediction-vs-reality settlement;
- scheduled refresh jobs and provider quota metrics;
- Claude adapter behind a feature flag and cost limits;
- accessibility, i18n baseline, and audit events.

## Phase 3 — analytical product

- ticket builder with explicit correlation/risk warnings;
- premium entitlements and billing;
- admin moderation/configuration UI;
- calibrated confidence and evaluation dashboards;
- notifications and saved analyses.

## Phase 4 — scale and governance

- additional sports/providers;
- model registry, approvals, drift monitoring, and explainability review;
- privacy automation, retention jobs, disaster recovery drills;
- jurisdiction-specific responsible-gambling controls.
