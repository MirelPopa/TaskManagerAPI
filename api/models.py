from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Enum as SQLEnum
from api.db import Base
from datetime import datetime


class TaskStatus(str, PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
