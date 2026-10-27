import sys
import threading
from typing import List, Optional, Dict


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def expected_solve(board):
    """Iterative reference: flood-fill from border 'O's, flip the rest."""
    rows, cols = len(board), len(board[0])
    res = [row[:] for row in board]
    safe = set()
    stack = []
    for r in range(rows):
        for c in range(cols):
            if (r in (0, rows - 1) or c in (0, cols - 1)) and res[r][c] == "O":
                stack.append((r, c))
                safe.add((r, c))
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and res[nr][nc] == "O" and (nr, nc) not in safe:
                safe.add((nr, nc))
                stack.append((nr, nc))
    for r in range(rows):
        for c in range(cols):
            if res[r][c] == "O" and (r, c) not in safe:
                res[r][c] = "X"
    return res


def grid(strs):
    return [list(s) for s in strs]


def snake(n):
    """Border-connected serpentine path of 'O's (deep recursion for naive DFS)."""
    b = [["X"] * n for _ in range(n)]
    for r in range(0, n, 2):
        for c in range(n):
            b[r][c] = "O"
    for r in range(1, n, 2):
        c = n - 1 if (r // 2) % 2 == 0 else 0
        b[r][c] = "O"
    return b


def enclosed_snake(n):
    """Serpentine path inside an 'X' frame: fully surrounded, must be captured."""
    inner = snake(n - 2)
    b = [["X"] * n for _ in range(n)]
    for r in range(n - 2):
        for c in range(n - 2):
            b[r + 1][c + 1] = inner[r][c]
    return b


def checker(n, m):
    return [["O" if (r + c) % 2 == 0 else "X" for c in range(m)] for r in range(n)]


def build_cases():
    cases = []
    # 1-2: examples
    cases.append(grid(["XXXX", "XOOX", "XXOX", "XOXX"]))
    cases.append(grid(["X"]))
    # 3: single O
    cases.append(grid(["O"]))
    # 4: single row of O
    cases.append(grid(["OOOO"]))
    # 5: single column
    cases.append([["O"], ["X"], ["O"]])
    # 6: 3x3 center O captured
    cases.append(grid(["XXX", "XOX", "XXX"]))
    # 7: 3x3 all O
    cases.append(grid(["OOO", "OOO", "OOO"]))
    # 8: 2x2 mixed
    cases.append(grid(["OX", "XO"]))
    # 9: interior region connected to border via chain
    cases.append(grid(["XXXXX", "XOOOX", "XOXOX", "XOXXX", "OXXXX"]))
    # 10: two interior regions, one touching border
    cases.append(grid(["XXXXXX", "XOXXOX", "XXXXXX", "XOOOOO", "XXXXXX"]))
    # 11: checkerboard
    cases.append(checker(7, 6))
    # 12: all X
    cases.append([["X"] * 5 for _ in range(4)])
    # 13: large all-O board
    cases.append([["O"] * 200 for _ in range(200)])
    # 14: large board, interior all O inside X frame
    b = [["X"] * 200 for _ in range(200)]
    for r in range(1, 199):
        for c in range(1, 199):
            b[r][c] = "O"
    cases.append(b)
    # 15: large serpentine connected to border (deep path)
    cases.append(snake(199))
    # 16: large serpentine fully enclosed
    cases.append(enclosed_snake(200))
    return cases


def run(ns, board):
    sol = ns["Solution"]()
    ret = sol.solve(board)
    return ret


def describe(board):
    if len(board) * len(board[0]) > 100:
        return f"<{len(board)}x{len(board[0])} board>"
    return str(board)


def main():
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
    exec(open("attempt.py").read(), ns)

    cases = build_cases()
    passed = 0
    for i, board in enumerate(cases, 1):
        want = expected_solve(board)
        inp = describe(board)
        work = [row[:] for row in board]
        try:
            run(ns, work)
        except BaseException as e:
            print(f"FAIL case {i}: input={inp}, error={type(e).__name__}: {e}")
            continue
        if work == want:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={inp}, expected={describe(want)}, got={describe(work)}")

    print(f"{passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    # Recursive DFS solutions need deep recursion on 200x200 boards; run with a big stack.
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    result = []
    t = threading.Thread(target=lambda: result.append(main()))
    t.start()
    t.join()
    sys.exit(result[0] if result else 1)