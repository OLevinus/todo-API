import json
import os
from typing import List, Optional
from models import Task

DATA_FILE = "tasks.json"


class TaskManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.tasks: List[Task] = self._load()

    # ---------- persistence ----------

    def _load(self) -> List[Task]:
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r") as f:
            raw = json.load(f)
        return [Task(**item) for item in raw]

    def _save(self):
        with open(self.data_file, "w") as f:
            json.dump([task.model_dump() for task in self.tasks], f, indent=2)

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    # ---------- CRUD ----------

    def list_tasks(self) -> List[Task]:
        return self.tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def add_task(self, title: str) -> Task:
        task = Task(id=self._next_id(), title=title, done=False)
        self.tasks.append(task)
        self._save()
        return task

    def update_task(self, task_id: int, title: Optional[str] = None,
                     done: Optional[bool] = None) -> Optional[Task]:
        task = self.get_task(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if done is not None:
            task.done = done
        self._save()
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self._save()
        return True
