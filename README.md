# CloudSport

CloudSport is an AI-assisted football prediction and analytical ticket platform.

## Phase 1

Phase 1 is a deliberately small vertical slice:

- football fixtures from API-Sports with PostgreSQL caching;
- stale-cache fallback when the provider is unavailable, unauthenticated, rate-limited, or suspended;
- deterministic Match Winner and Over/Under Goals predictions;
- persisted prediction history;
- optional Claude provider interface (disabled by default);
- minimal React fixture/prediction view.

See [`docs/phase-1.md`](docs/phase-1.md), [`docs/gap-analysis.md`](docs/gap-analysis.md), and [`docs/environment.md`](docs/environment.md).

## Run in Codespaces

```bash
cp .env.example .env
# Set DATABASE_URL and API_SPORTS_KEY in .env
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# in another terminal
cd frontend && npm install && npm run dev
```

PostgreSQL is required; SQLite is intentionally not supported.
