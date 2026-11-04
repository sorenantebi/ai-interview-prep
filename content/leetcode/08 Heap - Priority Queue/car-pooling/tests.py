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
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    # (trips, capacity, expected)
    ([[2, 1, 5], [3, 3, 7]], 4, False),
    ([[2, 1, 5], [3, 3, 7]], 5, True),
    ([[1, 0, 1]], 1, True),
    ([[5, 0, 10]], 4, False),
    # drop-off before pickup at the same kilometer
    ([[3, 0, 5], [3, 5, 10]], 3, True),
    # overlap of one kilometer
    ([[3, 0, 6], [3, 5, 10]], 5, False),
    # unsorted input, max load 6
    ([[3, 5, 8], [2, 0, 6], [4, 2, 4]], 6, True),
    ([[3, 5, 8], [2, 0, 6], [4, 2, 4]], 5, False),
    # nested trips, max load 9
    ([[2, 0, 10], [3, 1, 9], [4, 2, 8]], 8, False),
    ([[2, 0, 10], [3, 1, 9], [4, 2, 8]], 9, True),
    # same pickup point
    ([[1, 3, 6], [2, 3, 5], [3, 3, 4]], 6, True),
    # several drop-offs at the same point before a pickup
    ([[5, 0, 4], [5, 1, 4], [5, 4, 8]], 10, True),
    # large: 1000 sequential single-passenger trips
    ([[1, i, i + 1] for i in range(1000)], 1, True),
    # large: 1000 groups of 100 over the whole route
    ([[100, 0, 1000] for _ in range(1000)], 100000, True),
    ([[100, 0, 1000] for _ in range(1000)], 99999, False),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for n, (trips, cap, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.carPooling(copy.deepcopy(trips), cap)
        if got == expected and isinstance(got, bool):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(trips)}, capacity={cap}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(trips)}, capacity={cap}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
