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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "heapq": heapq,
}
exec(open("attempt.py").read(), ns)

N = 100000

cases = [
    ([[1, 2], [2, 4], [3, 2], [4, 1]], [0, 2, 3, 1]),
    ([[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]], [4, 3, 2, 0, 1]),
    ([[1, 1]], [0]),
    ([[1, 1], [10, 1], [5, 1]], [0, 2, 1]),
    ([[1, 3], [1, 3], [1, 3]], [0, 1, 2]),
    ([[5, 2], [1, 2], [3, 1]], [1, 2, 0]),
    ([[1, 10], [2, 1], [3, 1], [4, 1]], [0, 1, 2, 3]),
    ([[10**9, 10**9], [1, 10**9], [10**9, 1]], [1, 2, 0]),
    ([[1, 2], [3, 1], [3, 1]], [0, 1, 2]),
    ([[1, 5], [2, 3], [3, 1], [4, 2]], [0, 2, 3, 1]),
    ([[2, 1], [2, 1], [1, 1]], [2, 0, 1]),
    ([[i + 1, 1] for i in range(N)], list(range(N))),
    ([[1, N - i] for i in range(N)], list(range(N - 1, -1, -1))),
]


def show(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "...(truncated)"


passed = 0
total = len(cases)
for n, (tasks, expected) in enumerate(cases, 1):
    try:
        inp = [list(t) for t in tasks]
        got = ns["Solution"]().getOrder(inp)
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={show(tasks)}, expected={show(expected)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={show(tasks)}, expected={show(expected)}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)