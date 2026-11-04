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
Solution = ns["Solution"]

# Large inputs
big_all = [[r, c] for r in range(100) for c in range(100)]
big_even = [[r, c] for r in range(100) for c in range(100) if (r + c) % 2 == 0]
line_pos = [[0, i] for i in range(0, 10000, 2)] + [[0, i] for i in range(1, 10000, 2)]
line_exp = list(range(1, 5001)) + [5000 - k for k in range(1, 5000)] + [1]

cases = [
    (3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]], [1, 1, 2, 3]),
    (1, 1, [[0, 0]], [1]),
    (2, 2, [[0, 0], [0, 0], [1, 1], [1, 1]], [1, 1, 2, 2]),
    (3, 3, [[0, 0], [0, 2], [2, 0], [2, 2], [1, 1], [0, 1], [1, 0], [1, 2], [2, 1]],
     [1, 2, 3, 4, 5, 3, 2, 1, 1]),
    (1, 5, [[0, 0], [0, 2], [0, 4], [0, 1], [0, 3]], [1, 2, 3, 2, 1]),
    (5, 1, [[0, 0], [2, 0], [4, 0], [1, 0], [3, 0]], [1, 2, 3, 2, 1]),
    (3, 3, [[0, 0], [1, 1], [2, 2]], [1, 2, 3]),
    (3, 3, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0]], [1] * 8),
    (2, 3, [[0, 0], [1, 2], [0, 1], [0, 2], [0, 2]], [1, 2, 2, 1, 1]),
    (100, 100, big_all, [1] * 10000),
    (100, 100, big_even, list(range(1, 5001))),
    (1, 10000, line_pos, line_exp),
]


def show(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for i, (m, n, pos, exp) in enumerate(cases, 1):
    try:
        got = Solution().numIslands2(m, n, [p[:] for p in pos])
        if list(got) == exp:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input=({m}, {n}, {show(pos)}), expected={show(exp)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input=({m}, {n}, {show(pos)}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)