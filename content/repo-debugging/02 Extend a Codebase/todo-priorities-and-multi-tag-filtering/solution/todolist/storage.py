"""In-memory todo storage with JSON persistence."""

import json
from datetime import date
from typing import Dict, Iterable, List, Optional

from .models import Priority, Todo


class TodoNotFound(KeyError):
    """Raised when an id does not exist in the store."""


class TodoStore:
    """Keeps todos in insertion order and hands out incrementing ids."""

    def __init__(self) -> None:
        self._items: Dict[int, Todo] = {}
        self._next_id = 1

    def add(
        self,
        title: str,
        due: Optional[date] = None,
        tags: Iterable[str] = (),
        priority: Priority = Priority.MEDIUM,
    ) -> Todo:
        """Create a todo, store it and return it."""
        todo = Todo(
            id=self._next_id, title=title, due=due, tags=tags, priority=priority
        )
        self._items[todo.id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id: int) -> Todo:
        try:
            return self._items[todo_id]
        except KeyError:
            raise TodoNotFound(todo_id) from None

    def complete(self, todo_id: int) -> Todo:
        """Mark a todo as done and return it."""
        todo = self.get(todo_id)
        todo.done = True
        return todo

    def remove(self, todo_id: int) -> None:
        self.get(todo_id)
        del self._items[todo_id]

    def all(self) -> List[Todo]:
        """Return all todos in insertion order."""
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def dumps(self) -> str:
        """Serialise the whole store to a JSON string."""
        payload = {
            "next_id": self._next_id,
            "todos": [t.to_dict() for t in self.all()],
        }
        return json.dumps(payload)

    @classmethod
    def loads(cls, text: str) -> "TodoStore":
        """Rebuild a store from the output of :meth:`dumps`."""
        data = json.loads(text)
        store = cls()
        for item in data["todos"]:
            todo = Todo.from_dict(item)
            store._items[todo.id] = todo
        store._next_id = data["next_id"]
        return store
