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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out, q = [], [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

N = 10 ** 9

cases = [
    # 1: example from the problem
    ([(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)], [1, 1, 2, 3, 3, 3]),
    # 2: single event
    ([(0, 1)], [1]),
    # 3: touching events never overlap (half-open)
    ([(1, 2), (2, 3), (3, 4)], [1, 1, 1]),
    # 4: identical events stack
    ([(5, 10)] * 4, [1, 2, 3, 4]),
    # 5: nested events
    ([(0, 100), (10, 20), (12, 15), (13, 14)], [1, 2, 3, 4]),
    # 6: extreme bounds
    ([(0, N), (0, N), (N - 1, N)], [1, 2, 3]),
    # 7: touching then bridged
    ([(10, 20), (20, 30), (15, 25)], [1, 1, 2]),
    # 8: sliding window of length 10
    ([(i, i + 10) for i in range(20)], list(range(1, 11)) + [10] * 10),
    # 9: large, 400 nested events
    ([(i, N - i) for i in range(400)], list(range(1, 401))),
    # 10: large, 400 disjoint events
    ([(2 * i, 2 * i + 1) for i in range(400)], [1] * 400),
    # 11: reverse-order disjoint bookings
    ([(30, 40), (20, 30), (10, 20)], [1, 1, 1]),
    # 12: max reached, later events do not raise it
    ([(1, 5), (2, 6), (3, 7), (4, 8), (8, 9), (0, 1)], [1, 2, 3, 4, 4, 4]),
]

passed = 0
total = len(cases)
for idx, (ops, expected) in enumerate(cases, 1):
    shown = ops if len(ops) <= 10 else f"{len(ops)} bookings starting {ops[:3]}..."
    try:
        cal = ns["MyCalendarThree"]()
        got = [cal.book(s, e) for s, e in ops]
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            exp_s = expected if len(expected) <= 12 else f"{expected[:12]}..."
            got_s = got if len(got) <= 12 else f"{got[:12]}..."
            print(f"FAIL case {idx}: input={shown}, expected={exp_s}, got={got_s}")
    except Exception as ex:
        print(f"FAIL case {idx}: input={shown}, expected={expected[:12]}, got=error: {ex!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
