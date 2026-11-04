import sys
import heapq
import collections
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
    "collections": collections,
}
exec(open("attempt.py").read(), ns)


def build_snake():
    rows, cols = 99, 100
    big = 10**6
    grid = []
    for i in range(rows):
        if i % 2 == 0:
            grid.append([1] * cols)
        else:
            row = [big] * cols
            if i % 4 == 1:
                row[cols - 1] = 1
            else:
                row[0] = 1
            grid.append(row)
    return grid


def build_gradient():
    return [[1 + i + j for j in range(100)] for i in range(100)]


cases = [
    ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
    ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
    ([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]], 0),
    ([[5]], 0),
    ([[1, 10, 6, 100]], 94),
    ([[1], [3], [2]], 2),
    ([[1, 1000000]], 999999),
    ([[3, 3, 3], [3, 3, 3], [3, 3, 3]], 0),
    ([[1, 10], [10, 1]], 9),
    ([[1, 3], [4, 2]], 2),
    ([[1, 10, 6, 7, 9, 10, 4, 9]], 9),
    (build_snake(), 0),
    (build_gradient(), 1),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
total = len(cases)
for idx, (heights, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.minimumEffortPath([row[:] for row in heights])
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short(heights)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(heights)}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)