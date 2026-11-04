import sys
import math
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big = [[0] * 100 for _ in range(100)]
big[0][1] = 1

cases = [
    ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
    ([[0, 1], [0, 0]], 1),
    ([[0]], 1),
    ([[1]], 0),
    ([[0, 1]], 0),
    ([[1, 0]], 0),
    ([[0, 0], [0, 1]], 0),
    ([[1, 0], [0, 0]], 0),
    ([[0] * 5], 1),
    ([[0], [0], [0], [0], [0]], 1),
    ([[0] * 4 for _ in range(3)], 10),
    ([[0, 1, 0], [1, 0, 0], [0, 0, 0]], 0),
    ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], 1),
    ([[0] * 17 for _ in range(17)], math.comb(32, 16)),
    (big, math.comb(197, 98)),
]


def run():
    passed = 0
    total = len(cases)
    for i, (grid, expected) in enumerate(cases, 1):
        inp = [row[:] for row in grid]
        shown = grid if len(grid) <= 5 else f"<{len(grid)}x{len(grid[0])} grid>"
        try:
            sol = ns["Solution"]()
            got = sol.uniquePathsWithObstacles(inp)
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got=error: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()
