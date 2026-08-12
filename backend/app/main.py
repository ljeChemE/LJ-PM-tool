import os
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session

from app.clock import today
from app.db import engine, get_db
from app.models import Project, Task
from app.schemas import ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate

app = FastAPI(title="PM Tool API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unreachable: {exc}")
    return {"status": "ok"}


@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    project = Project(name=payload.name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return list(db.scalars(select(Project)).all())


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_today: date = Depends(today),
) -> Task:
    project = db.get(Project, payload.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    task = Task(
        title=payload.title,
        project_id=payload.project_id,
        deadline=payload.deadline or current_today,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks/today", response_model=list[TaskOut])
def list_todays_tasks(
    db: Session = Depends(get_db),
    current_today: date = Depends(today),
) -> list[Task]:
    # Roll forward anything still open from a day that's already passed —
    # this, not a background job, is what "passed to the daily standup"
    # means: it happens the moment today's list is asked for.
    db.execute(
        update(Task)
        .where(Task.deadline < current_today, Task.done.is_(False))
        .values(
            deadline=current_today,
            carried_over_count=Task.carried_over_count + 1,
        )
    )
    db.commit()

    return list(db.scalars(select(Task).where(Task.deadline == current_today)).all())


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks_for_day(day: date, db: Session = Depends(get_db)) -> list[Task]:
    return list(db.scalars(select(Task).where(Task.deadline == day)).all())


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task
