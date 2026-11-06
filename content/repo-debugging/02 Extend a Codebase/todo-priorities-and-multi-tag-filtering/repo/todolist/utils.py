"""Small helpers shared across the todolist package."""

from typing import FrozenSet, Iterable


def normalize_tag(tag: str) -> str:
    """Return the canonical form of a tag: trimmed and lower-case."""
    return tag.strip().lower()


def normalize_tags(tags: Iterable[str]) -> FrozenSet[str]:
    """Normalise an iterable of tags, dropping blanks and duplicates."""
    cleaned = (normalize_tag(t) for t in tags)
    return frozenset(t for t in cleaned if t)
