import sys
import copy
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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_py(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
    ([[1, 2, 3], [4, 5, 6]], 12),
    ([[5]], 5),
    ([[0]], 0),
    ([[1, 2, 3, 4]], 10),
    ([[1], [2], [3], [4]], 10),
    ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0),
    ([[1, 2], [1, 1]], 3),
    ([[9, 1, 1], [9, 9, 1], [9, 9, 1]], 13),
    ([[1, 100, 1], [1, 100, 1], [1, 1, 1]], 5),
    ([[1] * 200 for _ in range(200)], 399),
    ([[200] * 200 for _ in range(200)], 79800),
    ([[0 if (i == 0 or j == 199) else 200 for j in range(200)] for i in range(200)], 0),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
total = len(cases)
for idx, (grid, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.minPathSum(copy.deepcopy(grid))
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input={short(grid)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(grid)}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
