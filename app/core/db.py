from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create the SQLAlchemy engine using the DATABASE_URL from settings
# The `connect_args` is needed only for SQLite to allow multi-threaded access.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our declarative models
Base = declarative_base()

# Dependency Injector: provides a database session to an API endpoint
def get_db():
    """
    Yields a new database session for a single request, and ensures it's
    closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()