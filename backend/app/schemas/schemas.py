"""
Models for request/response validation using Pydantic.

Dependencies:
    - pydantic: For data validation and settings management
"""

from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    """
    Response model for file upload endpoint.
    """
    id: int
    link: str
    status: str


class FileOutputResponse(BaseModel):
    """
    Response model for file output endpoint.
    """
    id: int
    link: str
    text: str
    status: str


class FileRecord(BaseModel):
    """
    Base model for file records in database.
    """
    link: str
    status: str = "processing"
