from celery import Celery

celery_app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Automatically discover tasks in the 'tasks' module
celery_app.autodiscover_tasks(["app.tasks"])