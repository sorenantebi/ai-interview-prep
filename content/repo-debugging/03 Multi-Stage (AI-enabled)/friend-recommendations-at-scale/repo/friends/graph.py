"""In-memory social graph stored as adjacency sets."""

from typing import AbstractSet, Dict, FrozenSet, List, Set


class SocialGraph:
    """Undirected friendship graph over integer user ids."""

    def __init__(self) -> None:
        self._adj: Dict[int, Set[int]] = {}

    def add_user(self, user: int) -> None:
        """Make sure ``user`` exists, even without any friends."""
        self._adj.setdefault(user, set())

    def add_edge(self, source: int, target: int) -> None:
        """Record a one-way link ``source -> target``.

        This is a low-level building block; both users are registered, but
        only ``source`` gets ``target`` in its adjacency set. Use
        :meth:`add_friendship` to record a friendship.
        """
        self._adj.setdefault(source, set()).add(target)
        self._adj.setdefault(target, set())

    def add_friendship(self, a: int, b: int) -> None:
        """Record that ``a`` and ``b`` are friends (visible from both sides)."""
        if a == b:
            raise ValueError("a user cannot befriend themselves")
        self.add_edge(a, b)
        self.add_edge(b, a)

    def has_user(self, user: int) -> bool:
        return user in self._adj

    def users(self) -> List[int]:
        """All user ids in ascending order."""
        return sorted(self._adj)

    def friends_of(self, user: int) -> FrozenSet[int]:
        """Return a snapshot of ``user``'s friends. Raises ``KeyError`` if unknown."""
        return frozenset(self._adj[user])

    def neighbors(self, user: int) -> AbstractSet[int]:
        """Return the live adjacency set of ``user`` without copying it.

        Callers must not mutate the result. Raises ``KeyError`` if unknown.
        """
        return self._adj[user]

    def degree(self, user: int) -> int:
        return len(self._adj[user])

    def are_friends(self, a: int, b: int) -> bool:
        return b in self._adj.get(a, ())

    def __len__(self) -> int:
        return len(self._adj)
