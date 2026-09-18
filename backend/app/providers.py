import json, logging
from datetime import datetime, timedelta, timezone
import httpx
from sqlalchemy.orm import Session
from .config import settings
from .models import Fixture

logger = logging.getLogger(__name__)

class ApiSportsClient:
    def __init__(self, db: Session): self.db = db

    def fixtures(self, date: str | None = None) -> tuple[list[Fixture], str, str | None]:
        if settings.api_sports_key:
            try:
                response = httpx.get(f"{settings.api_sports_base_url}/fixtures", params={"date": date} if date else {}, headers={"x-apisports-key": settings.api_sports_key}, timeout=settings.api_sports_timeout_seconds)
                response.raise_for_status()
                payload = response.json()
                rows = [self._upsert(item) for item in payload.get("response", [])]
                self.db.commit()
                return rows, "live", None
            except (httpx.HTTPError, ValueError, KeyError) as exc:
                logger.warning("api_sports_failure", extra={"error": str(exc)})
        else:
            logger.warning("api_sports_key_missing")
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        cached = self.db.query(Fixture).filter(Fixture.fetched_at >= cutoff).order_by(Fixture.kickoff_at).limit(100).all()
        return cached, "stale" if cached else "unavailable", "API-Sports unavailable; cached fixtures may be stale."

    def _upsert(self, item: dict) -> Fixture:
        info, teams, league = item["fixture"], item.get("teams", {}), item.get("league", {})
        row = self.db.query(Fixture).filter_by(provider_id=info["id"]).first() or Fixture(provider_id=info["id"], sport="football")
        row.home_team, row.away_team = teams.get("home", {}).get("name", "Unknown"), teams.get("away", {}).get("name", "Unknown")
        row.league_name, row.kickoff_at, row.status = league.get("name"), datetime.fromisoformat(info["date"].replace("Z", "+00:00")), info.get("status", {}).get("short")
        row.raw_json, row.fetched_at = json.dumps(item), datetime.now(timezone.utc)
        self.db.add(row)
        return row
