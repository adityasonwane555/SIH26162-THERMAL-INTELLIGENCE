"""Database engine and session management with seamless SQLite fallback."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings, logger

Base = declarative_base()

def get_engine():
    db_url = settings.DATABASE_URL
    use_sqlite = False

    if settings.USE_SQLITE_FALLBACK:
        # Check if postgres is accessible
        if "postgresql" in db_url:
            try:
                import psycopg2
                test_engine = create_engine(db_url, connect_args={"connect_timeout": 2})
                with test_engine.connect() as conn:
                    logger.info("Connected successfully to PostgreSQL/PostGIS database.")
                    return test_engine
            except Exception as e:
                logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite database at {settings.SQLITE_DB_PATH}.")
                use_sqlite = True
        else:
            use_sqlite = True
    
    if use_sqlite or "sqlite" in db_url:
        sqlite_url = f"sqlite:///{settings.SQLITE_DB_PATH}"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})
    
    return create_engine(db_url)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes all database tables."""
    from src.database import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
