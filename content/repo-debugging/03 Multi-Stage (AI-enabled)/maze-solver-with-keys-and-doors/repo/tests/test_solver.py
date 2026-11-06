from maze.parser import parse_grid
from maze.solver import shortest_path

KEY_ON_ROUTE = """
#########
#S.a.A.G#
#########
"""

KEY_DETOUR = """
#######
#S.A.G#
#.#####
#a#####
#######
"""

AROUND_WALL = """
#######
#S.#.G#
#..#..#
#.....#
#######
"""


def test_straight_corridor():
    maze = parse_grid("#####\n#S.G#\n#####")
    assert shortest_path(maze) == [(1, 1), (1, 2), (1, 3)]


def test_goes_around_wall():
    maze = parse_grid(AROUND_WALL)
    path = shortest_path(maze)
    assert path is not None
    assert path[0] == maze.start and path[-1] == maze.goal
    assert len(path) == 9


def test_key_on_the_way_opens_door():
    maze = parse_grid(KEY_ON_ROUTE)
    assert shortest_path(maze) == [(1, c) for c in range(1, 8)]


def test_detour_to_fetch_key():
    maze = parse_grid(KEY_DETOUR)
    expected = [(1, 1), (2, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    assert shortest_path(maze) == expected


def test_door_without_key_is_unreachable():
    maze = parse_grid("#####\n#SAG#\n#####")
    assert shortest_path(maze) is None


def test_wrong_key_does_not_open_door():
    maze = parse_grid("#########\n#S.b.A.G#\n#########")
    assert shortest_path(maze) is None
