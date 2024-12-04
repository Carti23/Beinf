"""
Module for handling asynchronous file processing tasks using Celery and database operations.

Dependencies:
    - database: For database session management
    - models: Contains FileRecord model definition
    - celery: For asynchronous task processing
    - time: For simulating processing delays
"""

from app.database.database import SessionLocal
from app.models.models import FileRecord
import time
from celery import Celery

"""
Celery Configuration:
    broker: Redis instance running on localhost:6379/0
    backend: Same Redis instance for storing results
"""
celery_app = Celery(
    "app", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)

"""
Auto-discover tasks defined in the app.tasks module
This allows Celery to find and register all tasks automatically
"""
celery_app.autodiscover_tasks(["app.tasks"])


@celery_app.task
def process_file(record_id):
    """
    Asynchronous task for processing file records.

    Args:
        record_id (int): The ID of the FileRecord to process

    Flow:
        1. Creates database session
        2. Simulates processing with sleep
        3. Updates record status to 'done'
        4. Commits changes and closes session

    Returns:
        None

    Side Effects:
        - Updates FileRecord status in database
        - Closes database session in finally block
    """
    db = SessionLocal()
    try:
        time.sleep(10)

        record = db.query(FileRecord).filter(
            FileRecord.id == record_id).first()
        if record:
            record.status = "done"
            db.commit()
    finally:
        db.close()
