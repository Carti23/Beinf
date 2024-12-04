import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.models import FileRecord
from app.utils.s3_utils import upload_file_to_s3, download_file_from_s3
from app.tasks.tasks import process_file

# Utility function to generate a unique filename using a UUID


def generate_unique_filename(original_filename):
    """
    Generates a unique filename by appending a UUID to the original file's extension.

    Args:
        original_filename (str): The name of the original file.

    Returns:
        str: A unique filename.
    """
    file_extension = original_filename.split(".")[-1]
    return f"{uuid.uuid4()}.{file_extension}"

# Asynchronous function to handle file uploads and processing


async def process_upload(file: UploadFile, db: Session):
    """
    Handles the upload of a file, saves it temporarily, uploads it to S3, 
    creates a database record, and triggers an asynchronous task for further processing.

    Args:
        file (UploadFile): The uploaded file.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the file's ID, S3 link, and status.
    """
    # Generate a unique filename and temporary file path
    unique_filename = generate_unique_filename(file.filename)
    file_path = f"/tmp/{unique_filename}"

    # Save the file locally in the temporary directory
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Upload the file to S3 and get the S3 link
    file_link = upload_file_to_s3(file_path, unique_filename)

    # Create a new database record for the uploaded file
    record = FileRecord(link=file_link, status="processing")
    db.add(record)
    db.commit()
    db.refresh(record)

    # Remove the temporary file to free up space
    os.remove(file_path)

    # Trigger a Celery task to process the file asynchronously
    process_file.delay(record.id)

    # Return the file metadata and status
    return {"id": record.id, "link": record.link, "status": record.status}

# Function to retrieve file processing output from the database


def get_file_output(record_id: int, db: Session):
    """
    Retrieves the processed file's output based on its record ID, downloads it from S3, 
    and reads the content.

    Args:
        record_id (int): The ID of the file record in the database.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the file's ID, S3 link, content, and status.

    Raises:
        FileNotFoundError: If the record is not found in the database.
    """
    # Query the database for the file record by its ID
    record = db.query(FileRecord).filter(FileRecord.id == record_id).first()
    if not record:
        raise FileNotFoundError("Record not found")

    # Extract the filename from the S3 link and set a local file path
    file_name = record.link.split("/")[-1]
    local_file_path = f"/tmp/{file_name}"

    # Download the file from S3 to the local temporary directory
    download_file_from_s3(file_name, local_file_path)

    # Read the file's content
    with open(local_file_path, "r") as file:
        file_content = file.read()

    # Return the file metadata and content
    return {
        "id": record.id,
        "link": record.link,
        "text": file_content,
        "status": record.status,
    }
