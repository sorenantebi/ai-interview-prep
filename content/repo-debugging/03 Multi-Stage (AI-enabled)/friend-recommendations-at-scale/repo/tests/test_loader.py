from friends.loader import load_edges


def test_load_makes_friendship_visible_from_both_sides():
    g = load_edges(["1 2", "2 3"])
    assert g.are_friends(1, 2)
    assert g.are_friends(2, 1), "friendship should be mutual"
    assert g.are_friends(3, 2)


def test_load_degrees_are_symmetric():
    g = load_edges(["1 2", "1 3", "1 4"])
    assert g.degree(1) == 3
    assert g.degree(2) == 1
    assert g.friends_of(4) == frozenset({1})


def test_load_skips_comments_blanks_and_self_loops():
    g = load_edges(["# header", "", "1 2", "3 3", "  ", "2 3"])
    assert g.users() == [1, 2, 3]


def test_load_reports_line_number_of_bad_line():
    try:
        load_edges(["1 2", "oops"])
    except ValueError as exc:
        assert "line 2" in str(exc)
    else:
        assert False, "expected ValueError"
