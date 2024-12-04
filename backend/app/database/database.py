"""
Database configuration module for SQLAlchemy integration with PostgreSQL.

Dependencies:
    - SQLAlchemy: For database ORM functionality
    - PostgreSQL: Database backend
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL with PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"

# Create SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)

# Create sessionmaker factory configured for PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function to manage database sessions.

    Yields:
        Session: SQLAlchemy database session

    Side Effects:
        - Creates new database session
        - Ensures session closure after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
