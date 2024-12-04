from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services import file_service
from app.schemas.schemas import FileUploadResponse, FileOutputResponse

# Initialize a FastAPI router for file-related endpoints
router = APIRouter()


@router.post("/generate/", response_model=FileUploadResponse)
async def generate(file: UploadFile, db: Session = Depends(get_db)):
    """
    Endpoint to upload a file, process it, and store its metadata in the database.

    Args:
        file (UploadFile): The uploaded file from the request.
        db (Session): The database session dependency.

    Returns:
        FileUploadResponse: Contains file ID, link, and processing status.

    Raises:
        HTTPException: If any error occurs during file processing.
    """
    try:
        # Call the file service to process the upload and return the result
        return await file_service.process_upload(file, db)
    except Exception as e:
        # Handle unexpected errors and return a 500 Internal Server Error
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/output/{record_id}", response_model=FileOutputResponse)
def output(record_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve the processed file's output by its record ID.

    Args:
        record_id (int): The ID of the file record to retrieve.
        db (Session): The database session dependency.

    Returns:
        FileOutputResponse: Contains file metadata, content, and processing status.

    Raises:
        HTTPException: 
            - 404 Not Found: If the file record is not found in the database.
            - 500 Internal Server Error: If any other error occurs during retrieval.
    """
    try:
        # Call the file service to get the file output and return the result
        return file_service.get_file_output(record_id, db)
    except FileNotFoundError:
        # Handle case where the file record is not found and return 404 Not Found
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        # Handle unexpected errors and return a 500 Internal Server Error
        raise HTTPException(
            status_code=500, detail=f"Error retrieving file: {str(e)}")
