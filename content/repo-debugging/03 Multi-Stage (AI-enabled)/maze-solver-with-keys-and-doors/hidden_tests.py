import random
import time
from collections import deque

from maze.cli import solve_text
from maze.keys import door_bit, is_door, is_key, key_bit
from maze.parser import parse_grid
from maze.solver import shortest_path


# ---------------------------------------------------------------- helpers

def check_path(maze, path):
    assert path[0] == maze.start, "path must begin at the start"
    assert path[-1] == maze.goal, "path must end at the goal"
    mask = 0
    for i, pos in enumerate(path):
        assert maze.in_bounds(pos) and not maze.is_wall(pos), f"bad cell {pos}"
        if i:
            pr, pc = path[i - 1]
            assert abs(pr - pos[0]) + abs(pc - pos[1]) == 1, f"non-adjacent step at {i}"
        ch = maze.cell(pos)
        if is_door(ch):
            assert mask & door_bit(ch), f"door {ch} entered without key at step {i}"
        if is_key(ch):
            mask |= key_bit(ch)


def reference_steps(maze):
    start = (maze.start, frozenset())
    dist = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        pos, keys = state
        if pos == maze.goal:
            return dist[state]
        r, c = pos
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < maze.rows and 0 <= nc < maze.cols):
                continue
            ch = maze.grid[nr][nc]
            if ch == "#":
                continue
            if ch in "ABCDEF" and ch.lower() not in keys:
                continue
            nkeys = keys | {ch} if ch in "abcdef" else keys
            nstate = ((nr, nc), nkeys)
            if nstate not in dist:
                dist[nstate] = dist[state] + 1
                queue.append(nstate)
    return None


def random_maze_text(rng, rows, cols):
    pool = ["#"] * 3 + ["."] * 6 + ["a", "b", "A", "B"]
    grid = [[rng.choice(pool) for _ in range(cols)] for _ in range(rows)]
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    s, g = rng.sample(cells, 2)
    grid[s[0]][s[1]] = "S"
    grid[g[0]][g[1]] = "G"
    return "\n".join("".join(row) for row in grid)


def serpentine(rows, cols, items=None):
    """One long winding corridor; rows must be odd."""
    grid = [["#"] * cols for _ in range(rows)]
    n = (rows - 1) // 2
    for i in range(n):
        r = 2 * i + 1
        for c in range(1, cols - 1):
            grid[r][c] = "."
        if i < n - 1:
            grid[r + 1][cols - 2 if i % 2 == 0 else 1] = "."
    grid[1][1] = "S"
    end_col = cols - 2 if (n - 1) % 2 == 0 else 1
    grid[2 * (n - 1) + 1][end_col] = "G"
    for (r, c), ch in (items or {}).items():
        grid[r][c] = ch
    return "\n".join("".join(row) for row in grid)


def serpentine_steps(rows, cols):
    n = (rows - 1) // 2
    return n * (cols - 3) + 2 * (n - 1)


def timed(maze):
    t0 = time.perf_counter()
    path = shortest_path(maze)
    return path, time.perf_counter() - t0


# ---------------------------------------------------------------- parser

def test_tall_maze_positions():
    maze = parse_grid("###\n#S#\n#.#\n#.#\n#G#\n###")
    assert maze.rows == 6 and maze.cols == 3
    assert maze.start == (1, 1)
    assert maze.goal == (4, 1)


def test_wide_maze_start_in_corner():
    maze = parse_grid("S.......\n.......G")
    assert maze.start == (0, 0)
    assert maze.goal == (1, 7)


def test_crlf_and_trailing_whitespace():
    maze = parse_grid("\r\n#####  \r\n#S.G#\r\n#####\r\n\r\n")
    assert (maze.rows, maze.cols) == (3, 5)
    assert maze.goal == (1, 3)


def test_duplicate_start_rejected():
    try:
        parse_grid("#####\n#SSG#\n#####")
    except ValueError:
        return
    assert False, "expected ValueError"


def test_unknown_symbol_rejected():
    try:
        parse_grid("#####\n#SxG#\n#####")
    except ValueError:
        return
    assert False, "expected ValueError"


def test_neighbor_order():
    maze = parse_grid("S..\n...\n..G")
    assert list(maze.neighbors((1, 1))) == [(0, 1), (2, 1), (1, 0), (1, 2)]


# ---------------------------------------------------------------- solver

def test_start_next_to_goal():
    maze = parse_grid("####\n#SG#\n####")
    assert shortest_path(maze) == [(1, 1), (1, 2)]


def test_chain_of_keys_and_doors():
    maze = parse_grid("#############\n#S.a.A.b.B.G#\n#############")
    path = shortest_path(maze)
    assert path == [(1, c) for c in range(1, 12)]


def test_key_behind_its_own_door():
    maze = parse_grid("#######\n#S.AaG#\n#######")
    assert shortest_path(maze) is None


def test_solver_does_not_modify_maze():
    text = "#######\n#S.A.G#\n#.#####\n#a#####\n#######"
    maze = parse_grid(text)
    before = list(maze.grid)
    shortest_path(maze)
    assert maze.grid == before
    assert (maze.start, maze.goal) == ((1, 1), (1, 5))


def test_random_small_mazes_match_reference():
    rng = random.Random(0)
    for _ in range(60):
        maze = parse_grid(random_maze_text(rng, 6, 8))
        expected = reference_steps(maze)
        path = shortest_path(maze)
        if expected is None:
            assert path is None
        else:
            assert path is not None
            check_path(maze, path)
            assert len(path) - 1 == expected


def test_cli_reports_unreachable():
    assert solve_text("#####\n#SAG#\n#####") == "No path"


# ---------------------------------------------------------------- large inputs

def test_large_serpentine_with_keys():
    rows, cols = 251, 401
    items = {(1, 5): "a", (81, 200): "A", (121, 50): "b", (201, 300): "B"}
    maze = parse_grid(serpentine(rows, cols, items))
    path, elapsed = timed(maze)
    assert path is not None
    assert len(path) - 1 == serpentine_steps(rows, cols)
    check_path(maze, path)
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"


def test_large_serpentine_unreachable_goal():
    maze = parse_grid(serpentine(251, 401, {(1, 5): "a", (221, 200): "B"}))
    path, elapsed = timed(maze)
    assert path is None
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"


def test_large_open_grid():
    size = 200
    grid = ["." * size for _ in range(size)]
    grid[0] = "S" + grid[0][1:]
    grid[-1] = grid[-1][:-1] + "G"
    maze = parse_grid("\n".join(grid))
    path, elapsed = timed(maze)
    assert path is not None
    assert len(path) - 1 == 2 * (size - 1)
    check_path(maze, path)
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"


def test_large_maze_with_all_six_keys():
    rows, cols = 151, 201
    items = {}
    for i, letter in enumerate("abcdef"):
        items[(1, 3 + i)] = letter
        items[(61, 10 + i)] = letter.upper()
    maze = parse_grid(serpentine(rows, cols, items))
    path, elapsed = timed(maze)
    assert path is not None
    assert len(path) - 1 == serpentine_steps(rows, cols)
    check_path(maze, path)
    assert elapsed < 1.0, f"too slow: {elapsed:.2f}s"
