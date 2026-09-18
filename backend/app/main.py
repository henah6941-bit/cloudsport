from datetime import date as calendar_date
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models import Fixture, Prediction
from .predictions import RulePredictionEngine
from .providers import ApiSportsClient

app = FastAPI(title="CloudSport API", version="0.1.1")
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok", "prediction_provider": settings.prediction_provider}


@app.get("/api/fixtures")
def fixtures(fixture_date: str | None = Query(default=None, alias="date"), db: Session = Depends(get_db)):
    rows, source, warning = ApiSportsClient(db).fixtures(fixture_date or str(calendar_date.today()))
    provider = RulePredictionEngine()
    result = []
    for fixture in rows:
        predictions = []
        for item in provider.predict(fixture):
            existing = db.query(Prediction).filter_by(fixture_id=fixture.id, market=item.market, engine_version=provider.version).first()
            if existing is None:
                existing = Prediction(fixture_id=fixture.id, market=item.market, selection=item.selection, confidence=item.confidence, explanation=item.explanation, provider=provider.name, engine_version=provider.version)
                db.add(existing)
            else:
                existing.selection, existing.confidence, existing.explanation = item.selection, item.confidence, item.explanation
            predictions.append({"market": item.market, "selection": item.selection, "confidence": item.confidence, "explanation": item.explanation})
        result.append({"id": fixture.id, "provider_id": fixture.provider_id, "sport": fixture.sport, "home_team": fixture.home_team, "away_team": fixture.away_team, "league": fixture.league_name, "kickoff_at": fixture.kickoff_at, "source": source, "predictions": predictions})
    db.commit()
    return {"source": source, "stale": source == "stale", "warning": warning, "fixtures": result}
