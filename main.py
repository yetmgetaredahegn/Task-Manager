from typing import Dict
from datetime import datetime
from operator import ne
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None 

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)


app = FastAPI()


tasks: Dict[int, Task] = {}
next_id = 1

@app.get("/tasks")
async def list_tasks(
    completed: bool | None = Query(None),
    search: str | None = Query(None)
):
    results = list(tasks.values())

    if completed is not None:
        results = [t for t in results if t.completed == completed]

    if search:
        results = [t for t in results if search.lower() in t.title.lower()]

    return results


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

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate):
    task = tasks.get(task_id)
    if task is None:
        return {"error": "Task not found"}

    updated_task = task.model_copy(update=task_data.model_dump(exclude_unset=True))
    tasks[task_id] = updated_task
    return updated_task





@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task = tasks.pop(task_id, None)
    if task is None:
        return {"error": "Task not found"}
    return {"message": "Task deleted successfully"}


@app.patch("/tasks/{task_id}/toggle")
async def toggle_task_completion(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        return {"error": "Task not found"}

    updated_task = task.model_copy(update={"completed": not task.completed})
    tasks[task_id] = updated_task
    return updated_task

   
