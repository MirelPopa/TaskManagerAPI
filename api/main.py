from fastapi import FastAPI, Depends
from sqlalchemy.exc import SQLAlchemyError
from api.db import create_database_schema
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from api.db import get_db
from api.models import Task
from api.schema import TaskStatus, TaskBase, TaskRead, TaskCreate
from typing import List

router = FastAPI()
create_database_schema()


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
