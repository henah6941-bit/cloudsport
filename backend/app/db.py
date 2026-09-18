import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings

logging.basicConfig(level=settings.log_level)
engine = create_engine(settings.database_url.replace("postgres://", "postgresql+psycopg://").replace("postgresql://", "postgresql+psycopg://"), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
