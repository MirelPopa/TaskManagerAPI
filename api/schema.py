from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from api.models import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime

    class Config:
        orm_mode = True
