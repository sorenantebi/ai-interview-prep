from maze.parser import parse_grid

CORRIDOR = """
#####
#S.G#
#####
"""


def test_parse_dimensions():
    maze = parse_grid(CORRIDOR)
    assert maze.rows == 3
    assert maze.cols == 5


def test_parse_start_and_goal_positions():
    maze = parse_grid(CORRIDOR)
    assert maze.start == (1, 1)
    assert maze.goal == (1, 3), "positions are (row, col)"


def test_parse_ignores_blank_edge_lines():
    maze = parse_grid("\n\n" + CORRIDOR + "\n\n")
    assert maze.rows == 3


def test_parse_rejects_missing_start():
    try:
        parse_grid("###\n#.G\n###")
    except ValueError:
        return
    assert False, "expected ValueError"


def test_parse_rejects_ragged_rows():
    try:
        parse_grid("#####\n#S.G\n#####")
    except ValueError:
        return
    assert False, "expected ValueError"


def test_neighbors_skip_walls():
    maze = parse_grid(CORRIDOR)
    assert list(maze.neighbors(maze.goal)) == [(1, 2)]
