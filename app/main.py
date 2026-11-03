
from typing import Annotated

from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


from fastapi import Query
from sqlalchemy import select

from fastapi import HTTPException


app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/v1/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_task = Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task



@app.get("/api/v1/tasks", response_model=list[TaskResponse])
def list_tasks(
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    is_completed: bool | None = None,
):
    statement = select(Task)

    if is_completed is not None:
        statement = statement.where(
            Task.is_completed == is_completed
        )

    statement = (
        statement
        .order_by(Task.id)
        .offset(skip)
        .limit(limit)
    )

    tasks = db.scalars(statement).all()

    return tasks


@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task


@app.patch("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updates: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    update_data = updates.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title cannot be null",
        )

    if "is_completed" in update_data and update_data["is_completed"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="is_completed cannot be null",
        )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@app.delete(
    "/api/v1/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    db.delete(task)
    db.commit()
