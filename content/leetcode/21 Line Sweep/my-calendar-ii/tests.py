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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_array(head):
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
MyCalendarTwo = ns["MyCalendarTwo"]

BIG = 10 ** 9

cases = [
    # 1: example from the problem
    ([(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)],
     [True, True, True, False, True, True]),
    # 2: single event
    ([(0, 1)], [True]),
    # 3: identical events, third is rejected
    ([(1, 5), (1, 5), (1, 5)], [True, True, False]),
    # 4: adjacent intervals are not overlapping
    ([(10, 20), (20, 30), (10, 30), (15, 25), (0, 10), (30, 40)],
     [True, True, True, False, True, True]),
    # 5: touching at the boundary of a double booking
    ([(1, 3), (2, 4), (3, 5), (2, 3), (4, 5), (3, 4)],
     [True, True, True, False, True, False]),
    # 6: large coordinates
    ([(0, BIG), (0, BIG), (BIG - 1, BIG), (0, 1)],
     [True, True, False, False]),
    # 7: nested intervals
    ([(10, 50), (20, 30), (25, 28), (40, 45), (30, 40), (0, 10), (29, 31)],
     [True, True, False, True, True, True, False]),
    # 8: filling gaps between singles
    ([(1, 2), (3, 4), (5, 6), (1, 6), (2, 3), (0, 7)],
     [True, True, True, True, True, False]),
    # 9: partial overlaps
    ([(0, 5), (3, 8), (6, 10), (4, 7), (5, 6), (5, 7)],
     [True, True, True, False, True, False]),
    # 10: repeated identical unit events
    ([(0, 1), (0, 1), (0, 1), (0, 1)], [True, True, False, False]),
    # 11: rejected events are not stored
    ([(1, 3), (2, 4), (2, 3), (3, 4), (1, 2)],
     [True, True, False, True, True]),
    # 12: large input, 900 calls
    ([(2 * i, 2 * i + 1) for i in range(300)]
     + [(2 * i, 2 * i + 1) for i in range(300)]
     + [(2 * i, 2 * i + 1) for i in range(300)]
     + [(0, BIG)],
     [True] * 300 + [True] * 300 + [False] * 300 + [False]),
]


def short(x):
    s = str(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
for n, (ops, expected) in enumerate(cases, 1):
    try:
        cal = MyCalendarTwo()
        got = [cal.book(s, e) for s, e in ops]
        got = [bool(g) if isinstance(g, bool) else g for g in got]
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(ops)}, expected={short(expected)}, got={short(got)}")
    except Exception as ex:
        print(f"FAIL case {n}: input={short(ops)}, error={type(ex).__name__}: {ex}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
