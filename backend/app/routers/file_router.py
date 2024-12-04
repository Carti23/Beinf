from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services import file_service
from app.schemas.schemas import FileUploadResponse, FileOutputResponse

router = APIRouter()

@router.post("/generate/", response_model=FileUploadResponse)
async def generate(file: UploadFile, db: Session = Depends(get_db)):
    try:
        return await file_service.process_upload(file, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/output/{record_id}", response_model=FileOutputResponse)
def output(record_id: int, db: Session = Depends(get_db)):
    try:
        return file_service.get_file_output(record_id, db)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")