
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.models import Base


# Load the project-root .env regardless of the
# directory from which Uvicorn is started.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db",
).strip()


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is empty. Check your project-root .env file."
    )


# Normalize PostgreSQL URL for the installed psycopg2 driver.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg2://",
        1,
    )

elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1,
    )


# Configure the appropriate connection.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
    )

elif DATABASE_URL.startswith("postgresql+psycopg2://"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=3,
        max_overflow=2,
        pool_recycle=1800,
        connect_args={
            "sslmode": "require",
        },
    )

else:
    raise RuntimeError(
        "Unsupported DATABASE_URL scheme. "
        "Use SQLite or PostgreSQL with psycopg2."
    )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def init_db():
    """Create missing application tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a database session to FastAPI endpoints."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()