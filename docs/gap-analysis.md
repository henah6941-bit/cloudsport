# Provisional requirements gap analysis

The two referenced requirements documents were not available as readable file attachments in the repository/session, so this is a **provisional** analysis based only on the supplied summary and decisions. It must be reconciled against the full A–AT and 47–57 documents before implementing later phases.

## Decisions now resolved

- Python/FastAPI backend, React frontend, PostgreSQL from day one.
- No authentication in Phase 1.
- Football first, with a sport dimension in the schema.
- Persist predictions rather than calculating only on request.
- Rule-based provider active; Anthropic adapter optional and disabled.
- Match Winner and Over/Under Goals only in the initial fallback engine.
- API provider failures use cached fixtures and expose a stale flag.

## Risks and ambiguities to resolve before Phase 2

1. **Prediction contract:** exact market settlement rules, void/postponed handling, odds source, bookmaker selection, and timezone policy need one canonical definition.
2. **Data licensing:** API-Sports terms, retention limits, redistribution rights, and whether raw provider payloads may be stored/displayed need legal confirmation.
3. **AI claims:** confidence calibration, explanation wording, model/version traceability, evaluation datasets, human oversight, and the boundary between information and gambling advice must be specified.
4. **Responsible gambling:** age/geo controls, self-exclusion, spending limits, risk warnings, and jurisdiction-specific obligations are not safe to infer.
5. **Billing:** provider, tax/VAT treatment, webhook idempotency, refunds, trials, entitlement expiry, and chargeback behavior require a concrete design.
6. **Authorization:** admin/support/moderator roles, tenant boundaries, audit events, and break-glass access need a permission matrix.
7. **Privacy:** retention/deletion/export workflows, consent records, processor inventory, breach response, and data residency need explicit owners and deadlines.
8. **Operations:** SLOs, alert destinations, backup/restore targets, migration rollback, API budget/rate limits, and Render free-tier sleep behavior need acceptance criteria.
9. **Internationalization:** supported locales, translation ownership, number/date/timezone formats, and right-to-left requirements should be narrowed for MVP.
10. **Ticket semantics:** maximum legs, duplicate fixtures, correlation risk, stake/profit calculations, and whether tickets are merely analytical or actionable must be explicit.

## Solo-developer realism

Defer payments, full admin, custom ML training, multi-sport parity, social features, live/in-play prediction, automated retraining, and jurisdiction-specific gambling workflows. Build observability and data provenance early, but keep the first UI read-only and avoid user funds or wagering execution.
