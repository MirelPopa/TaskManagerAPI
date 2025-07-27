import os
import time

from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("worker", broker=redis_url)


@app.task
def generate_report(task_id: int) -> str:
    print(f"Generating report for task {task_id}...")
    time.sleep(5)
    return f"Report for task {task_id} generated successfully!"
