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


def build_list(values):
    dummy = node = ListNode()
    for v in values:
        node.next = ListNode(v)
        node = node.next
    return dummy.next


def serialize_list(head, limit=1000):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        if len(out) > limit:
            raise RuntimeError("list too long, possible cycle")
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]

cases = [
    ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
    ([], [], []),
    ([], [0], [0]),
    ([0], [], [0]),
    ([5], [1], [1, 5]),
    ([1], [1], [1, 1]),
    ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([4, 5, 6], [1, 2, 3], [1, 2, 3, 4, 5, 6]),
    ([-100, -50, 0], [-75, -50, 100], [-100, -75, -50, -50, 0, 100]),
    ([2, 2, 2], [2, 2], [2, 2, 2, 2, 2]),
    ([1, 3, 5, 7, 9], [2], [1, 2, 3, 5, 7, 9]),
    (list(range(-100, -50)), list(range(50, 100)), list(range(-100, -50)) + list(range(50, 100))),
    (list(range(0, 100, 2))[:50], list(range(1, 100, 2))[:50], list(range(100))),
]

passed = 0
total = len(cases)
for i, (a, b, expected) in enumerate(cases, 1):
    try:
        got = serialize_list(Solution().mergeTwoLists(build_list(a), build_list(b)))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={a}, {b}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={a}, {b}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)