from friends.graph import SocialGraph


def test_add_friendship_is_mutual():
    g = SocialGraph()
    g.add_friendship(1, 2)
    assert g.are_friends(1, 2)
    assert g.are_friends(2, 1)


def test_friends_of_returns_snapshot():
    g = SocialGraph()
    g.add_friendship(1, 2)
    g.add_friendship(1, 3)
    assert g.friends_of(1) == frozenset({2, 3})


def test_friends_of_unknown_user_raises():
    g = SocialGraph()
    try:
        g.friends_of(42)
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"


def test_self_friendship_rejected():
    g = SocialGraph()
    try:
        g.add_friendship(5, 5)
    except ValueError:
        pass
    else:
        assert False, "expected ValueError"


def test_add_user_without_friends():
    g = SocialGraph()
    g.add_user(9)
    assert g.has_user(9)
    assert g.degree(9) == 0
    assert len(g) == 1
