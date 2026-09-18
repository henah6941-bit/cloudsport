import json
import logging
from datetime import datetime, timezone
from typing import Any

import httpx
from sqlalchemy.orm import Session

from .config import settings
from .models import Fixture, Sport, utcnow

logger = logging.getLogger(__name__)


class ProviderError(RuntimeError):
    """A provider failure safe to expose as a stale-cache response."""


class ApiSportsClient:
    def __init__(self, db: Session, transport: Any = httpx):
        self.db = db
        self.transport = transport

    def fixtures(self, fixture_date: str | None = None) -> tuple[list[Fixture], str, str | None]:
        failure_reason = "API-Sports unavailable; cached fixtures may be stale."
        if not settings.api_sports_key:
            logger.warning("api_sports_key_missing")
        else:
            try:
                response = self.transport.get(
                    f"{settings.api_sports_base_url.rstrip('/')}/fixtures",
                    params={"date": fixture_date} if fixture_date else {},
                    headers={"x-apisports-key": settings.api_sports_key},
                    timeout=settings.api_sports_timeout_seconds,
                )
                if response.status_code in (401, 403):
                    failure_reason = "API-Sports rejected the credentials or account access. Cached fixtures are being served."
                elif response.status_code == 429:
                    failure_reason = "API-Sports rate limit reached. Cached fixtures are being served."
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict) or not isinstance(payload.get("response", []), list):
                    raise ValueError("API-Sports returned an unexpected payload")
                rows = [self._upsert(item) for item in payload["response"]]
                self._ensure_sport()
                self.db.commit()
                return rows, "live", None
            except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
                logger.warning("api_sports_failure", extra={"error_type": type(exc).__name__, "error": str(exc)})
        cached = self.db.query(Fixture).order_by(Fixture.kickoff_at).limit(100).all()
        return cached, "stale" if cached else "unavailable", failure_reason if cached else "API-Sports unavailable and no cached fixtures exist."

    def _ensure_sport(self) -> None:
        if not self.db.query(Sport).filter_by(code="football").first():
            self.db.add(Sport(code="football", name="Football"))

    def _upsert(self, item: dict[str, Any]) -> Fixture:
        info = item["fixture"]
        teams, league = item.get("teams", {}), item.get("league", {})
        fixture_date = datetime.fromisoformat(info["date"].replace("Z", "+00:00"))
        if fixture_date.tzinfo is None:
            fixture_date = fixture_date.replace(tzinfo=timezone.utc)
        row = self.db.query(Fixture).filter_by(provider_id=info["id"]).first()
        if row is None:
            row = Fixture(provider_id=info["id"], sport="football", home_team="Unknown", away_team="Unknown", kickoff_at=fixture_date)
        row.home_team = teams.get("home", {}).get("name", "Unknown")
        row.away_team = teams.get("away", {}).get("name", "Unknown")
        row.league_name = league.get("name")
        row.kickoff_at = fixture_date
        row.status = info.get("status", {}).get("short")
        row.raw_json = json.dumps(item)
        row.fetched_at = utcnow()
        self.db.add(row)
        return row
