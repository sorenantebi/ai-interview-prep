from maze.cli import solve_text
from maze.parser import parse_grid
from maze.render import format_solution, render_path

KEY_ON_ROUTE = """
#########
#S.a.A.G#
#########
"""

PATH = [(1, c) for c in range(1, 8)]


def test_render_marks_only_floor_cells():
    maze = parse_grid(KEY_ON_ROUTE)
    assert render_path(maze, PATH) == "#########\n#S*a*A*G#\n#########"


def test_format_solution_without_path():
    maze = parse_grid(KEY_ON_ROUTE)
    assert format_solution(maze, None) == "No path"


def test_solve_text_prints_steps_and_route():
    expected = "Steps: 6\n#########\n#S*a*A*G#\n#########"
    assert solve_text(KEY_ON_ROUTE) == expected
