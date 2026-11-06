"""Data model for a single todo item."""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Optional

from .utils import normalize_tags


@dataclass
class Todo:
    """A task with an optional due date and a set of free-form tags."""

    id: int
    title: str
    due: Optional[date] = None
    tags: frozenset = field(default_factory=frozenset)
    done: bool = False

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")
        self.tags = normalize_tags(self.tags)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation."""
        return {
            "id": self.id,
            "title": self.title,
            "due": self.due.isoformat() if self.due else None,
            "tags": sorted(self.tags),
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Todo":
        """Rebuild a todo from the output of :meth:`to_dict`."""
        due = data.get("due")
        return cls(
            id=data["id"],
            title=data["title"],
            due=date.fromisoformat(due) if due else None,
            tags=data.get("tags", []),
            done=data.get("done", False),
        )
