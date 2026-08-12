from datetime import date

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TaskCreate(BaseModel):
    title: str
    project_id: int
    deadline: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    deadline: date | None = None
    done: bool | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    project_id: int
    deadline: date
    done: bool
    carried_over_count: int
