from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Sport(Base):
    __tablename__ = "sports"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))


class Fixture(Base):
    __tablename__ = "fixtures"
    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    sport: Mapped[str] = mapped_column(String(32), default="football", index=True)
    league_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    home_team: Mapped[str] = mapped_column(String(150))
    away_team: Mapped[str] = mapped_column(String(150))
    kickoff_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    home_form: Mapped[float | None] = mapped_column(Float, nullable=True)
    away_form: Mapped[float | None] = mapped_column(Float, nullable=True)
    home_goals_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    away_goals_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (UniqueConstraint("fixture_id", "market", "engine_version"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    fixture_id: Mapped[int] = mapped_column(ForeignKey("fixtures.id", ondelete="CASCADE"), index=True)
    market: Mapped[str] = mapped_column(String(50))
    selection: Mapped[str] = mapped_column(String(100))
    confidence: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(50), default="rules")
    engine_version: Mapped[str] = mapped_column(String(50), default="rules-v1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
