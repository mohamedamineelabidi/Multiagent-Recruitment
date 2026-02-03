"""
Database Configuration

This module sets up the SQLAlchemy database connection and session management.
Supports both PostgreSQL (production) and SQLite (development).

Usage:
    from app.core.db import get_db, Base
    
    # In endpoint
    def my_endpoint(db: Session = Depends(get_db)):
        ...
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
# SQLite requires special connection args for multi-threading
_connect_args = (
    {"check_same_thread": False}
    if "sqlite" in settings.DATABASE_URL
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,  # Verify connections before use
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    Yields a database session and ensures it's closed after the request.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()