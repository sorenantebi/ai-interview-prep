import sys
import inspect
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


def tree_to_list(root):
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


def get_solver():
    # The solution may be wrapped in a class Solution, or be a bare function that still takes `self`.
    if "Solution" in ns and hasattr(ns["Solution"], "minMeetingRooms"):
        return ns["Solution"]().minMeetingRooms
    fn = ns["minMeetingRooms"]
    params = list(inspect.signature(fn).parameters)
    if params and params[0] == "self":
        return lambda intervals: fn(None, intervals)
    return fn


cases = [
    ([[0, 30], [5, 10], [15, 20]], 2),
    ([[7, 10], [2, 4]], 1),
    ([[1, 5], [2, 6], [3, 7], [5, 8]], 3),
    ([[1, 2]], 1),
    ([[1, 2], [2, 3], [3, 4]], 1),
    ([[1, 10]] * 5, 5),
    ([[1, 10], [2, 9], [3, 8], [4, 7]], 4),
    ([[0, 1], [2, 3], [4, 5]], 1),
    ([[1, 4], [4, 5], [2, 4]], 2),
    ([[0, 10**6], [0, 1], [1, 2]], 2),
    ([[i, i + 1] for i in range(10000)], 1),
    ([[0, 10**6] for _ in range(10000)], 10000),
    ([[i, i + 3] for i in range(10000)], 3),
]

passed = 0
total = len(cases)
for n, (intervals, expected) in enumerate(cases, 1):
    shown = intervals if len(intervals) <= 10 else f"<{len(intervals)} intervals>"
    try:
        solver = get_solver()
        got = solver([list(x) for x in intervals])
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
