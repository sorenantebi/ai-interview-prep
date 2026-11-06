from friends.graph import SocialGraph
from friends.service import FriendService


def test_mutual_friends_sorted():
    g = SocialGraph()
    for a, b in [(1, 3), (1, 2), (4, 2), (4, 3), (4, 9)]:
        g.add_friendship(a, b)
    svc = FriendService(g)
    assert svc.mutual_friends(1, 4) == [2, 3]
    assert svc.mutual_friends(4, 1) == [2, 3]


def test_service_recommend_from_edge_lines():
    svc = FriendService.from_edge_lines(["1 2", "2 3", "1 4", "4 3", "3 5"])
    assert svc.are_friends(2, 1)
    assert svc.recommend(1, 5) == [(3, 2)]
