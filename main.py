from typing import Dict
from datetime import datetime
from operator import ne
from fastapi import FastAPI
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None


app = FastAPI()


tasks: Dict[int, Task] = {}
next_id = 1

@app.get("/tasks")
async def list_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        return {"error": "Task not found"}
    return task

@app.post("/tasks")
async def create_task(task_data: TaskCreate):
    global next_id

    new_task = Task(
        id=next_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.now()
    )

    tasks[next_id] = new_task
    next_id += 1

    return new_task
   
