import json
from pathlib import Path
from typing import List
from .models import Task


class TaskStorage:
    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)
        self._tasks: List[Task] = []
        self.load()

    def load(self) -> None:
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._tasks = [Task.from_dict(item) for item in data]
        else:
            self._tasks = []

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._tasks], f, ensure_ascii=False, indent=2)

    def get_all(self) -> List[Task]:
        return self._tasks.copy()

    def add(self, task: Task) -> None:
        self._tasks.append(task)
        self.save()

    def get_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self._tasks if t.id == task_id), None)

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            self._tasks.remove(task)
            self.save()
            return True
        return False

    def next_id(self) -> int:
        if not self._tasks:
            return 1
        return max(t.id for t in self._tasks) + 1
