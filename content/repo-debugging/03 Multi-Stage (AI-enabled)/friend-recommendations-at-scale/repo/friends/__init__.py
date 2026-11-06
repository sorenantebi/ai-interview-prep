"""Friend recommendations over a social graph loaded from edge lists."""

from .graph import SocialGraph
from .loader import load_edges, load_file
from .recommender import Recommendation, recommend_friends
from .service import FriendService

__all__ = [
    "SocialGraph",
    "load_edges",
    "load_file",
    "Recommendation",
    "recommend_friends",
    "FriendService",
]
