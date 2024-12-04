"""
SQLAlchemy model definition for file records in the database.

Dependencies:
    - sqlalchemy: For ORM functionality and column types
    - database: Contains Base class for SQLAlchemy models

Table: file_records
    Stores information about processed files and their status
"""

from sqlalchemy import Column, Integer, String
from app.database.database import Base


class FileRecord(Base):
    """
    FileRecord model representing the file_records table.

    Attributes:
        id (int): Primary key, auto-incrementing identifier
        link (str): Unique link to the file, indexed for faster lookups
        status (str): Current processing status, defaults to "processing"

    Table Properties:
        - __tablename__: Specifies the table name in the database
        - Indexes on id and link columns for query optimization
        - Unique constraint on link column
    """
    __tablename__ = "file_records"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, unique=True, index=True)
    status = Column(String, default="processing")
