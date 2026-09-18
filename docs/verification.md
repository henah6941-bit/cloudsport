# Phase 1 verification

From the Codespaces terminal:

```bash
cp .env.example .env
# Set DATABASE_URL to a reachable PostgreSQL database.
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
curl -i http://localhost:8000/health
curl -s http://localhost:8000/api/fixtures | python -m json.tool
```

Expected health response includes `status: ok` and `database: ok`.

For live verification, set `API_SPORTS_KEY`, restart the API, and request `/api/fixtures?date=YYYY-MM-DD`. The response should contain `source: live`, fixtures, and two predictions per fixture.

For stale fallback verification, first obtain at least one live response so a fixture is cached. Then temporarily remove or invalidate `API_SPORTS_KEY` and call the endpoint again. Expected response: `source: stale`, `stale: true`, a warning, and cached fixtures. With no cached rows, the response is `source: unavailable` rather than a server error.

To confirm persistence, query PostgreSQL:

```sql
SELECT count(*) FROM fixtures;
SELECT fixture_id, market, selection, confidence, provider, engine_version
FROM predictions ORDER BY created_at DESC;
```

Run tests with PostgreSQL available:

```bash
cd backend
pytest -q
```
