"""Service layer used by the web handlers."""

from typing import Iterable, List

from .graph import SocialGraph
from .loader import load_edges
from .recommender import Recommendation, recommend_friends


class FriendService:
    """Thin facade over a :class:`SocialGraph`."""

    def __init__(self, graph: SocialGraph) -> None:
        self.graph = graph

    @classmethod
    def from_edge_lines(cls, lines: Iterable[str]) -> "FriendService":
        return cls(load_edges(lines))

    def are_friends(self, a: int, b: int) -> bool:
        return self.graph.are_friends(a, b)

    def mutual_friends(self, a: int, b: int) -> List[int]:
        """Sorted ids of the friends ``a`` and ``b`` have in common."""
        return sorted(self.graph.neighbors(a) & self.graph.neighbors(b))

    def recommend(self, user: int, k: int = 10) -> List[Recommendation]:
        return recommend_friends(self.graph, user, k)
