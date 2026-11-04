import sys
import copy
from typing import List, Optional, Dict

sys.setrecursionlimit(100000)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def comb(n):
    g = [[0] * n for _ in range(n)]
    for j in range(n):
        g[0][j] = 1
    for i in range(n):
        for j in range(0, n, 2):
            g[i][j] = 1
    return g


def short(grid):
    s = repr(grid)
    return s if len(s) <= 120 else s[:117] + "..."


cases = [
    ([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]], 16),
    ([[1]], 4),
    ([[1, 0]], 4),
    ([[1, 1]], 6),
    ([[1], [1], [1]], 8),
    ([[1, 1], [1, 1]], 8),
    ([[1, 1, 1], [1, 0, 1], [1, 1, 1]], 16),
    ([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 12),
    ([[1, 1, 0], [0, 1, 1]], 10),
    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 4),
    ([[1] * 100], 202),
    ([[1] * 100 for _ in range(100)], 400),
    (comb(100), 10102),
]

passed = 0
total = len(cases)
for n, (grid, expected) in enumerate(cases, 1):
    try:
        arg = copy.deepcopy(grid)
        got = ns["Solution"]().islandPerimeter(arg)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(grid)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(grid)}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)