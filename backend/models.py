from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    """What the client sends when creating a task."""
    title: str


class TaskUpdate(BaseModel):
    """What the client sends when updating a task. Both fields optional
    so you can update just the title, just 'done', or both."""
    title: Optional[str] = None
    done: Optional[bool] = None


class Task(BaseModel):
    """What the API sends back."""
    id: int
    title: str
    done: bool = False
