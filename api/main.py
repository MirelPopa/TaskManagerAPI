import time
from typing import List
from prometheus_client import start_http_server, Counter, Summary, generate_latest, CONTENT_TYPE_LATEST

from fastapi import Depends, FastAPI, Response
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.db import get_db
from api.models import Task
from api.schema import TaskBase, TaskCreate, TaskRead, TaskStatus
from worker.main import generate_report


REQUEST_COUNT = Counter("request_count", "Total number of requests")
REQUEST_LATENCY = Summary("request_latency_seconds", "Latency of requests in seconds")
router = FastAPI()


@router.middleware("http")
async def prometheus_middleware(request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.observe(latency)
    return response

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get(path="/tasks", response_model=List[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    stmt = select(Task)
    tasks = db.execute(stmt).scalars().all()
    return tasks


@router.post(path="/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    stmt = insert(Task).values(**task.model_dump()).returning(Task.id)
    try:
        result = db.execute(stmt)
        db.commit()
        inserted_id = result.scalar_one_or_none()
        if inserted_id is not None:
            return {"status": "success", "id": inserted_id}
        else:
            return {
                "status": "Failed",
                "reason": "Task already exists or violates constraints",
            }
    except SQLAlchemyError as e:
        db.rollback()
        return {"status": "Failed", "reason": str(e)}


@router.post("/tasks/{task_id}/generate-report")
def generate_report_endpoint(task_id: int):
    result = generate_report.delay(task_id)
    return {"task_id": task_id, "celery_id": result.id}
