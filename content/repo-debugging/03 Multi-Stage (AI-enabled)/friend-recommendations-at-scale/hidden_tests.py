import random
import time

from friends.graph import SocialGraph
from friends.loader import load_edges
from friends.recommender import Recommendation, recommend_friends
from friends.service import FriendService


def _graph(edges):
    g = SocialGraph()
    for a, b in edges:
        g.add_friendship(a, b)
    return g


def _brute(graph, user, k):
    friends = graph.friends_of(user)
    scored = []
    for cand in graph.users():
        if cand == user or cand in friends:
            continue
        m = len(friends & graph.friends_of(cand))
        if m:
            scored.append((-m, cand))
    scored.sort()
    return [(c, -m) for m, c in scored[:k]]


_BIG = {}


def _big_graph():
    if "g" not in _BIG:
        rng = random.Random(0)
        n = 100_000
        lines = []
        for _ in range(300_000):
            a, b = rng.randrange(n), rng.randrange(n)
            lines.append(f"{a} {b}")
        for _ in range(5_000):  # user 0 is very popular
            lines.append(f"0 {rng.randrange(1, n)}")
        _BIG["g"] = load_edges(lines)
    return _BIG["g"]


# ---- loader -------------------------------------------------------------

def test_loader_duplicate_and_reversed_edges():
    g = load_edges(["1 2", "2 1", "1 2"])
    assert g.degree(1) == 1 and g.degree(2) == 1
    assert g.are_friends(2, 1)


def test_loader_tabs_and_extra_whitespace():
    g = load_edges(["  1\t2  ", "3    4"])
    assert g.are_friends(2, 1) and g.are_friends(4, 3)


def test_loader_accepts_generator():
    g = load_edges(f"{i} {i + 1}" for i in range(5))
    assert g.degree(3) == 2
    assert g.friends_of(5) == frozenset({4})


def test_loader_rejects_wrong_field_count():
    try:
        load_edges(["1 2", "3 4", "1 2 3"])
    except ValueError as exc:
        assert "line 3" in str(exc)
    else:
        assert False, "expected ValueError"


def test_loader_rejects_non_integer_ids():
    try:
        load_edges(["a b"])
    except ValueError as exc:
        assert "line 1" in str(exc)
    else:
        assert False, "expected ValueError"


def test_loader_self_loop_does_not_create_user():
    g = load_edges(["7 7", "1 2"])
    assert not g.has_user(7)


# ---- recommender edge cases ---------------------------------------------

def test_k_zero_and_negative():
    g = _graph([(1, 2), (2, 3)])
    assert recommend_friends(g, 1, 0) == []
    assert recommend_friends(g, 1, -3) == []


def test_k_larger_than_candidates():
    g = _graph([(1, 2), (2, 3), (2, 4)])
    assert recommend_friends(g, 1, 100) == [(3, 1), (4, 1)]


def test_isolated_user_has_no_recommendations():
    g = _graph([(2, 3)])
    g.add_user(1)
    assert recommend_friends(g, 1, 5) == []


def test_unknown_user_raises_even_with_k_zero():
    g = _graph([(1, 2)])
    try:
        recommend_friends(g, 5, 0)
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"


def test_returns_recommendation_tuples():
    g = _graph([(1, 2), (2, 3)])
    res = recommend_friends(g, 1, 3)
    assert res == [Recommendation(3, 1)]
    assert res[0].user_id == 3 and res[0].mutual_friends == 1


def test_does_not_modify_graph():
    g = _graph([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])
    before = {u: set(g.friends_of(u)) for u in g.users()}
    recommend_friends(g, 1, 5)
    recommend_friends(g, 4, 5)
    after = {u: set(g.friends_of(u)) for u in g.users()}
    assert before == after


def test_matches_brute_force_on_random_graph():
    rng = random.Random(0)
    lines = [f"{rng.randrange(300)} {rng.randrange(300)}" for _ in range(1200)]
    g = load_edges(lines)
    for user in g.users():
        for k in (1, 5, 1000):
            assert recommend_friends(g, user, k) == _brute(g, user, k), (user, k)


def test_service_end_to_end_with_ties():
    svc = FriendService.from_edge_lines(
        ["1 2", "1 3", "2 9", "3 7", "2 8", "3 8", "# done"])
    assert svc.recommend(1, 2) == [(8, 2), (7, 1)]
    assert svc.mutual_friends(2, 3) == [1, 8]


# ---- large inputs -------------------------------------------------------

def test_large_random_queries_are_fast():
    g = _big_graph()
    rng = random.Random(1)
    sample = rng.sample(g.users(), 150)
    start = time.perf_counter()
    for user in sample:
        recommend_friends(g, user, 10)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"


def test_large_results_match_brute_force():
    g = _big_graph()
    rng = random.Random(2)
    for user in [0] + rng.sample(g.users(), 2):
        assert recommend_friends(g, user, 7) == _brute(g, user, 7), user


def test_popular_user_is_fast():
    g = _big_graph()
    start = time.perf_counter()
    res = recommend_friends(g, 0, 10)
    res_all = recommend_friends(g, 0, 10 ** 6)
    elapsed = time.perf_counter() - start
    assert len(res) == 10 and res_all[:10] == res
    counts = [r.mutual_friends for r in res_all]
    assert counts == sorted(counts, reverse=True)
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"


def test_star_graph_is_fast():
    g = SocialGraph()
    for leaf in range(1, 100_001):
        g.add_friendship(0, leaf)
    start = time.perf_counter()
    leaf_result = recommend_friends(g, 50_000, 5)
    center_result = recommend_friends(g, 0, 5)
    elapsed = time.perf_counter() - start
    assert leaf_result == [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    assert center_result == []
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"
