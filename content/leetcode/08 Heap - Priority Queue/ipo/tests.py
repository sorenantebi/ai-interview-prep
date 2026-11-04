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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_py(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "heapq": heapq,
}
exec(open("attempt.py").read(), ns)

cases = [
    # (k, w, profits, capital, expected)
    (2, 0, [1, 2, 3], [0, 1, 1], 4),
    (3, 0, [1, 2, 3], [0, 1, 2], 6),
    (1, 0, [1], [0], 1),
    (1, 0, [5], [1], 0),
    (5, 0, [1, 2, 3], [1, 1, 2], 0),
    (10, 0, [1, 2, 3], [0, 1, 2], 6),
    (3, 5, [0, 0, 0], [0, 5, 6], 5),
    (2, 2, [5, 3, 4], [3, 1, 2], 11),
    (3, 0, [1, 1, 1, 100], [0, 1, 2, 1000], 3),
    (2, 0, [1, 10, 100], [0, 1, 2], 11),
    (1, 10**9, [10000, 10000, 10000], [10**9, 10**9, 10**9 + 1], 10**9 + 10000),
    (10**5, 0, [1] * 10**5, list(range(10**5)), 10**5),
    (10**5, 0, [10000] * 10**5, [0] * 10**5, 10**9),
]

passed = 0
total = len(cases)
for n, (k, w, p, c, exp) in enumerate(cases, 1):
    desc = f"k={k}, w={w}, profits={p if len(p) <= 10 else '<len %d>' % len(p)}, capital={c if len(c) <= 10 else '<len %d>' % len(c)}"
    try:
        got = ns["Solution"]().findMaximizedCapital(k, w, list(p), list(c))
        if got == exp:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={desc}, expected={exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={desc}, expected={exp}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
