import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cloudsport_test")
from app.db import Base

@pytest.fixture
def db_session():
    engine = create_engine(os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://"))
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
