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

big_n = 20000
big_path = [[i, i + 1] for i in range(big_n - 1)]
big_star = [[0, i] for i in range(1, big_n)]

cases = [
    # (n, edges, expected)
    (4, [[1, 0], [1, 2], [1, 3]], [1]),
    (6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]], [3, 4]),
    (1, [], [0]),
    (2, [[0, 1]], [0, 1]),
    (3, [[0, 1], [1, 2]], [1]),
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]], [2]),
    (6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]], [2, 3]),
    (7, [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6]], [0]),
    (5, [[0, 3], [3, 1], [1, 4], [4, 2]], [1]),
    (7, [[0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [0, 6]], [0, 1]),
    (big_n, big_path, [9999, 10000]),
    (big_n, big_star, [0]),
]

passed = 0
total = len(cases)
for i, (n, edges, expected) in enumerate(cases, 1):
    label = f"n={n}, edges={edges if n < 100 else '<large>'}"
    exp_show = expected
    try:
        got = ns["Solution"]().findMinHeightTrees(n, [list(e) for e in edges])
        if sorted(got) == sorted(expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={label}, expected={exp_show}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={label}, expected={exp_show}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)