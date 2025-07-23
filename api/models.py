from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime
from api.db import Base
from datetime import datetime

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
