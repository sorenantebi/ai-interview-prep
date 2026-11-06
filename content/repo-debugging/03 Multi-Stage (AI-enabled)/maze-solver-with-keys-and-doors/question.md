---
difficulty: Hard
kind: multi-stage
---
# Maze Solver with Keys and Doors

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Hard

## Scenario
The `maze` package loads ASCII mazes (`#` wall, `.` floor, `S` start, `G` goal, lowercase `a`-`f` keys, uppercase `A`-`F` doors) and is meant to print the shortest route from `S` to `G`. The level designers have started feeding it rectangular mazes that are not square, and the positions it reports for the start and goal look wrong. The solver itself has never been written, and the designers want to run it on very large generated levels.

## Your tasks
1. **Stage 1, fix the bug.** Maze loading gives wrong results for some mazes. Find and fix the cause (the failing tests in `tests/test_parser.py` show the symptoms).
2. **Stage 2, implement the feature.** Implement `shortest_path` in `maze/solver.py`. A key is picked up by stepping on it, and a door can only be entered if the key with the same letter has been collected. Return the shortest route as a list of `(row, col)` cells from start to goal, or `None` if the goal cannot be reached. Once it works, `python -m maze.cli` should print the step count and the maze with the route drawn on it.
3. **Stage 3, make it fast.** Hidden tests run mazes with tens of thousands of cells and long winding routes (also unreachable goals), each with a time budget of about one second. Make sure your solver stays well inside it.

## Notes
- Positions are `(row, col)` everywhere, with `(0, 0)` at the top left.
- Moves are up, down, left and right only. Every step costs 1. Keys stay in the maze after pickup (stepping on them again does nothing).
- At most six key colours exist (`a`-`f`). `maze/keys.py` has the helpers for them.
- Entry points: `maze.parser.parse_grid`, `maze.solver.shortest_path`, `maze.cli.solve_text`.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
