from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------
# Database URL
# -----------------------------
# This will create (or use) backend/Data.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./Data.db"  # relative to backend/

# -----------------------------
# Create SQLAlchemy engine
# -----------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite specific
)

# -----------------------------
# Create SessionLocal
# -----------------------------
# Used in CRUD and FastAPI dependency
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# Base class for models
# -----------------------------
Base = declarative_base()

# -----------------------------
# Dependency for FastAPI
# -----------------------------
def get_db():
    """
    FastAPI dependency.
    Provides a session for the request and closes it automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
