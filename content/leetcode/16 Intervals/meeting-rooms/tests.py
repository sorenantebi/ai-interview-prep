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

big_ok = [[2 * i, 2 * i + 1] for i in range(9999, -1, -1)]
big_bad = [[2 * i, 2 * i + 1] for i in range(9999, -1, -1)] + [[2, 4]]
big_touch = [[i, i + 1] for i in range(9999, -1, -1)]

cases = [
    ([[0, 30], [5, 10], [15, 20]], False),
    ([[7, 10], [2, 4]], True),
    ([[5, 8], [8, 10]], True),
    ([], True),
    ([[1, 2]], True),
    ([[1, 2], [1, 2]], False),
    ([[1, 10], [2, 3]], False),
    ([[10, 12], [0, 5], [5, 10]], True),
    ([[1, 5], [4, 6]], False),
    ([[20, 30], [0, 10], [9, 12]], False),
    ([[0, 1000000]], True),
    ([[0, 500000], [500000, 1000000]], True),
    (big_ok, True),
    (big_bad, False),
    (big_touch, True),
]

passed = 0
total = len(cases)
for n, (intervals, expected) in enumerate(cases, 1):
    short = intervals if len(intervals) <= 10 else f"<{len(intervals)} intervals>"
    try:
        got = ns["Solution"]().canAttendMeetings(copy.deepcopy(intervals))
        if got == expected and isinstance(got, bool):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
