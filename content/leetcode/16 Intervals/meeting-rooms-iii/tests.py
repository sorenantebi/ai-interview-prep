import sys
import heapq
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
      "Optional": Optional, "Dict": Dict, "heapq": heapq}
exec(open("attempt.py").read(), ns)

cases = [
    (2, [[0, 10], [1, 5], [2, 7], [3, 4]], 0),
    (3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]], 1),
    (1, [[0, 1]], 0),
    (1, [[0, 5], [1, 2], [3, 4]], 0),
    (2, [[0, 1], [2, 3]], 0),
    (3, [[5, 6]], 0),
    (2, [[0, 5], [1, 2]], 0),
    (2, [[5, 6], [0, 10], [1, 2]], 1),
    (2, [[0, 10], [1, 3], [2, 4], [3, 5]], 1),
    (2, [[0, 10], [1, 2], [2, 3]], 1),
    (2, [[0, 500000]] + [[i, i + 1] for i in range(1, 100000)], 1),
    (3, [[i, i + 3] for i in range(100000)], 0),
]


def run():
    sol = ns["Solution"]()
    passed = 0
    for idx, (n, meetings, expected) in enumerate(cases, 1):
        label = f"n={n}, meetings={meetings if len(meetings) <= 10 else '<%d meetings>' % len(meetings)}"
        try:
            got = sol.mostBooked(n, [list(m) for m in meetings])
            if got == expected:
                print(f"PASS case {idx}")
                passed += 1
            else:
                print(f"FAIL case {idx}: input={label}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {idx}: input={label}, expected={expected}, got=error: {e!r}")
    print(f"{passed}/{len(cases)} passed")
    if passed != len(cases):
        sys.exit(1)


run()