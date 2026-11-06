from friends.graph import SocialGraph
from friends.recommender import recommend_friends


def _graph(edges):
    g = SocialGraph()
    for a, b in edges:
        g.add_friendship(a, b)
    return g


EXAMPLE = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5),
           (2, 6), (3, 6), (4, 7), (7, 8)]


def test_ranks_by_mutual_friends():
    g = _graph(EXAMPLE)
    assert recommend_friends(g, 1, 10) == [(5, 3), (6, 2), (7, 1)]


def test_limits_to_k():
    g = _graph(EXAMPLE)
    assert recommend_friends(g, 1, 2) == [(5, 3), (6, 2)]


def test_ties_broken_by_smaller_id():
    g = _graph([(1, 2), (1, 3), (2, 9), (3, 7), (2, 8), (3, 8)])
    assert recommend_friends(g, 1, 10) == [(8, 2), (7, 1), (9, 1)]


def test_excludes_existing_friends_and_self():
    g = _graph([(1, 2), (1, 3), (2, 3), (3, 4), (2, 4)])
    assert recommend_friends(g, 1, 10) == [(4, 2)]


def test_unknown_user_raises_key_error():
    g = _graph([(1, 2)])
    try:
        recommend_friends(g, 99, 5)
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"
