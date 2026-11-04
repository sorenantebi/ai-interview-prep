import sys
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

M = 2**31 - 1

cases = [
    ([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
     [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
    ([[0, 2, 3], [2, 5, 3]], [[0, 3], [5, 0]]),
    ([[1, 2, 1]], [[1, 1], [2, 0]]),
    ([[0, 2, 3], [5, 7, 4]], [[0, 3], [2, 0], [5, 4], [7, 0]]),
    ([[1, 5, 3], [1, 5, 5]], [[1, 5], [5, 0]]),
    ([[0, 10, 5], [2, 4, 3]], [[0, 5], [10, 0]]),
    ([[1, 5, 3], [2, 5, 6]], [[1, 3], [2, 6], [5, 0]]),
    ([[0, 3, 3], [1, 3, 2], [2, 3, 1]], [[0, 3], [3, 0]]),
    ([[0, 2, 1], [1, 3, 2], [2, 4, 3]], [[0, 1], [1, 2], [2, 3], [4, 0]]),
    ([[0, M, M]], [[0, M], [M, 0]]),
    ([[0, 2, 3], [2, 4, 5]], [[0, 3], [2, 5], [4, 0]]),
    ([[0, 2, 5], [1, 4, 3]], [[0, 5], [2, 3], [4, 0]]),
    ([[0, 3, 2], [1, 5, 2]], [[0, 2], [5, 0]]),
    ([[i, i + 2, 1] for i in range(10000)], [[0, 1], [10001, 0]]),
    ([[i, i + 1, i + 1] for i in range(10000)],
     [[i, i + 1] for i in range(10000)] + [[10000, 0]]),
]

passed = 0
total = len(cases)
for n, (inp, exp) in enumerate(cases, 1):
    desc = str(inp) if len(str(inp)) < 200 else f"<{len(inp)} buildings>"
    try:
        sol = ns["Solution"]()
        got = sol.getSkyline([list(b) for b in inp])
        got_norm = [list(p) for p in got]
        if got_norm == exp:
            print(f"PASS case {n}")
            passed += 1
        else:
            gs = str(got_norm) if len(str(got_norm)) < 200 else f"<{len(got_norm)} points>"
            es = str(exp) if len(str(exp)) < 200 else f"<{len(exp)} points>"
            print(f"FAIL case {n}: input={desc}, expected={es}, got={gs}")
    except Exception as e:
        print(f"FAIL case {n}: input={desc}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)