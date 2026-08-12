from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict

ProjectStatus = Literal["in_progress", "completed"]
TaskStatus = Literal["todo", "in_progress", "done"]


class ProjectCreate(BaseModel):
    name: str


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: ProjectStatus


class TaskCreate(BaseModel):
    title: str
    project_id: int
    deadline: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    deadline: date | None = None
    status: TaskStatus | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    project_id: int
    deadline: date
    status: TaskStatus
    carried_over_count: int
