# Environment

Copy `.env.example` to `.env` in Codespaces. Never commit secrets.

| Variable | Required | Description |
|---|---:|---|
| `DATABASE_URL` | yes | PostgreSQL URL. Render commonly supplies `postgresql://`; the app normalizes it to psycopg. |
| `API_SPORTS_KEY` | no | API-Sports `x-apisports-key`; without it, cached data is served. |
| `API_SPORTS_BASE_URL` | no | Defaults to `https://v3.football.api-sports.io`. |
| `API_SPORTS_TIMEOUT_SECONDS` | no | Defaults to `10`. |
| `CORS_ORIGINS` | no | Comma-separated browser origins; defaults to localhost Vite. |
| `PREDICTION_PROVIDER` | no | `rules` by default. `anthropic` is reserved and disabled until implemented/configured. |
| `ANTHROPIC_API_KEY` | no | Not used by Phase 1. |
| `LOG_LEVEL` | no | Defaults to `INFO`. |

The API key is sent only as a request header. Provider errors, including 401/403/429/5xx and timeouts, are logged without exposing the key and cause a database cache fallback.
