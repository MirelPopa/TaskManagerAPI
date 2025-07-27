import os
import time

from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery("worker", broker=redis_url)


@app.task
def process_task(task_id: int):
    print(f"Processing task {task_id}")
    time.sleep(5)  # simulate long-running task
    print(f"Finished task {task_id}")
    return {"status": "done"}
