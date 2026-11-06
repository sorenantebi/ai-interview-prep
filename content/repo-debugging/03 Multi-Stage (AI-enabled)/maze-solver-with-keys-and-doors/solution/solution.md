# Maze Solver with Keys and Doors - Solution

## Root causes / approach

**Stage 1: `maze/parser.py`, `_locate`.** The helper walked the grid with `y` for the row and `x` for the column and returned `(x, y)`. Everything else in the package (`Maze`, `neighbors`, `cell`, the renderer) uses `(row, col)`. On a square maze with the start on the diagonal nothing looks wrong, but the goal in `#S.G#` came back as `(3, 1)` instead of `(1, 3)`. That is out of bounds on a 3-row grid, so `neighbors(goal)` returned nothing, and the solver would have started from or aimed at the wrong cells. Fix: return `(row, col)` from `_locate`.

**Stage 2: `maze/solver.py`, `shortest_path`.** With keys, the cell alone is not enough as BFS state, because the same cell can be useful with different key sets (the detour test walks over `(1, 1)` twice, once without and once with key `a`). The search state is `(cell, key_mask)`, where `key_mask` is an int with one bit per key (`keys.key_bit` / `keys.door_bit`). BFS from `(start, 0)`:
- a neighbour that is a door is skipped unless its bit is in the mask;
- a neighbour that is a key sets its bit in the new mask;
- the first time a state with `cell == goal` is popped, it is on a shortest route (all steps cost 1).

A `parent` dict maps each state to its predecessor and doubles as the visited set. `_rebuild` follows the links back and keeps only the cells. The code reuses `Maze.neighbors`, `keys.py`, and the existing renderer / CLI, so `python -m maze.cli` prints the result without further changes.

**Stage 3: performance.** The usual slow version copies the whole route into every queue entry (`queue.append((pos, mask, path + [pos]))`). On a winding route of 50,000 cells that is O(L) work per state, so O(N * L) overall, in the billions of operations. Another common mistake is a visited set keyed by position only, which is fast but wrong (it breaks the key detour). The solution stores one parent pointer per state and reconstructs the route once at the end:
- before: O(N * L) time and memory churn for route copies;
- after: O(N * 2^k) states worst case with k <= 6 keys, but in practice every state is visited once and each costs O(1) (4 neighbours). The large tests have about 50,000 states and run in roughly 0.1-0.2 s.

Small constant-factor choices used here: ints as key sets (hashing a tuple of `(cell, int)` is cheap), and `grid` read directly in the loop.

## How to find it

1. Run the tests. Only the parser tests and the solver stub fail, so start with the parser. `test_parse_start_and_goal_positions` fails on the goal but not on the start, which hints at a row/column mix-up rather than a wrong search for `S` or `G`.
2. Print `maze.start` and `maze.goal` for a non-square input. `(3, 1)` for a goal in a 3-row maze is impossible. Follow `parse_grid` into `_locate` and compare the tuple order with `Maze` (its docstring says `(row, col)`).
3. Fix it and implement the solver. Check `test_detour_to_fetch_key`: if it fails with a visited set on positions only, the state needs the key mask.
4. For speed, time the solver on a long serpentine maze. If the time grows much faster than the cell count, look for per-state list copies and replace them with parent pointers.
