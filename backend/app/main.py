from datetime import date
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .db import Base, engine, get_db
from .models import Fixture, Prediction
from .predictions import RulePredictionEngine
from .providers import ApiSportsClient

Base.metadata.create_all(bind=engine)
app = FastAPI(title="CloudSport API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(__import__("sqlalchemy").text("SELECT 1"))
    return {"status": "ok", "database": "ok", "prediction_provider": settings.prediction_provider}

@app.get("/api/fixtures")
def fixtures(date: str | None = Query(default=None), db: Session = Depends(get_db)):
    rows, source, warning = ApiSportsClient(db).fixtures(date or str(date.today()))
    engine = RulePredictionEngine()
    result = []
    for fixture in rows:
        predictions = []
        for item in engine.predict(fixture):
            existing = db.query(Prediction).filter_by(fixture_id=fixture.id, market=item.market, engine_version=engine.version).first()
            if not existing:
                existing = Prediction(fixture_id=fixture.id, market=item.market, selection=item.selection, confidence=item.confidence, explanation=item.explanation, provider="rules", engine_version=engine.version)
                db.add(existing)
            predictions.append({"market": item.market, "selection": item.selection, "confidence": item.confidence, "explanation": item.explanation})
        result.append({"id": fixture.id, "provider_id": fixture.provider_id, "home_team": fixture.home_team, "away_team": fixture.away_team, "league": fixture.league_name, "kickoff_at": fixture.kickoff_at, "predictions": predictions})
    db.commit()
    return {"source": source, "warning": warning, "fixtures": result}
