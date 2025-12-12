from fastapi import FastAPI

app = FastAPI()

tasks = {
    1: "Task One",
    2: "Task Two"
}

@app.get("/tasks")
async def list_tasks():
    if not tasks:
        return {"error": "No tasks available"}
    return {"tasks": tasks}

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        return {"error": "Task not found"}
    return {"id": task_id, "title": task}
