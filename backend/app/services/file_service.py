import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.models import FileRecord
from app.utils.s3_utils import upload_file_to_s3, download_file_from_s3
from app.tasks.tasks import process_file

def generate_unique_filename(original_filename):
    file_extension = original_filename.split(".")[-1]
    return f"{uuid.uuid4()}.{file_extension}"

async def process_upload(file: UploadFile, db: Session):
    unique_filename = generate_unique_filename(file.filename)
    file_path = f"/tmp/{unique_filename}"
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_link = upload_file_to_s3(file_path, unique_filename)

    record = FileRecord(link=file_link, status="processing")
    db.add(record)
    db.commit()
    db.refresh(record)

    os.remove(file_path)

    process_file.delay(record.id)

    return {"id": record.id, "link": record.link, "status": record.status}

def get_file_output(record_id: int, db: Session):
    record = db.query(FileRecord).filter(FileRecord.id == record_id).first()
    if not record:
        raise FileNotFoundError("Record not found")

    file_name = record.link.split("/")[-1]
    local_file_path = f"/tmp/{file_name}"
    download_file_from_s3(file_name, local_file_path)
    
    with open(local_file_path, "r") as file:
        file_content = file.read()

    return {
        "id": record.id,
        "link": record.link,
        "text": file_content,
        "status": record.status,
    }