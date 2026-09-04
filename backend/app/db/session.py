"""
InsightPilot AI — Database Session Management
Manages engine initialization, connection pooling, and scoped session creation.
Supports PostgreSQL with seamless SQLite fallback for local testing.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Environment-driven database URL (Default to SQLite in data directory for zero-dependency local runs)
DEFAULT_SQLITE_PATH = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
    "data",
    "insightpilot.db"
)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")

# Engine configuration
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Initializes all database tables registered with Base metadata."""
    from backend.app.db.base import Base
    import backend.app.db.models  # Ensure models are imported so metadata is populated
    Base.metadata.create_all(bind=engine)
