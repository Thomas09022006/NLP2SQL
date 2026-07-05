import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config.config import settings

# Engine configured with Connection Pooling parameters
engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

# Read-only engine for executing AI-generated queries
readonly_db_url = os.getenv("READONLY_DATABASE_URL", settings.database_url)
readonly_engine = create_engine(
    readonly_db_url,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI Dependency to get database session.
    Ensures session is closed after request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
