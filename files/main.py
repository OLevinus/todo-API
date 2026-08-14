from fastapi import FastAPI, HTTPException
from models import Task, TaskCreate, TaskUpdate
from task_manager import TaskManager

app = FastAPI(title="To-Do API")
manager = TaskManager()


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    """Return all tasks."""
    return manager.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Return a single task by id, or 404 if it doesn't exist."""
    task = manager.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """Create a new task."""
    return manager.add_task(payload.title)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    """Update a task's title and/or done status."""
    task = manager.update_task(task_id, title=payload.title, done=payload.done)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task."""
    deleted = manager.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
