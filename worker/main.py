from celery import Celery
import time

app = Celery("worker", broker="redis://redis:6379/0")

@app.task
def process_task(task_id: int):
    print(f"Processing task {task_id}")
    time.sleep(5)  # simulate long-running task
    print(f"Finished task {task_id}")
    return {"status": "done"}
