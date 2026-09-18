import json
from unittest.mock import Mock
from app.models import Fixture
from app.providers import ApiSportsClient


def test_provider_returns_cached_rows_on_rate_limit(db_session, monkeypatch):
    cached = Fixture(provider_id=1, sport="football", home_team="A", away_team="B", kickoff_at="2026-01-01T00:00:00+00:00")
    db_session.add(cached); db_session.commit()
    response = Mock(status_code=429); response.raise_for_status.side_effect = Exception("429")
    monkeypatch.setattr("app.providers.settings.api_sports_key", "key")
    monkeypatch.setattr("app.providers.httpx.get", Mock(return_value=response))
    rows, source, warning = ApiSportsClient(db_session).fixtures("2026-01-01")
    assert rows and source == "stale" and "rate limit" in warning.lower()


def test_provider_returns_unavailable_without_key(db_session, monkeypatch):
    monkeypatch.setattr("app.providers.settings.api_sports_key", None)
    rows, source, warning = ApiSportsClient(db_session).fixtures("2026-01-01")
    assert rows == [] and source == "unavailable" and warning
