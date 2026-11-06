"""Friend recommendations based on mutual friends."""

from typing import List, NamedTuple

from .graph import SocialGraph


class Recommendation(NamedTuple):
    """A suggested friend and how many friends they share with the user."""

    user_id: int
    mutual_friends: int


def recommend_friends(graph: SocialGraph, user: int, k: int = 10) -> List[Recommendation]:
    """Return up to ``k`` friend suggestions for ``user``.

    Candidates are users who are not ``user`` and not already friends with
    ``user``, and who share at least one friend with ``user``. They are ranked
    by number of mutual friends (descending); ties are broken by smaller user
    id first.

    Raises ``KeyError`` if ``user`` is not in the graph. Returns an empty list
    when ``k <= 0`` or there are no candidates. The graph must not be modified.
    """
    raise NotImplementedError
