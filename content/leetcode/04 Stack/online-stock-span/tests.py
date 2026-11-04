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
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


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
StockSpanner = ns["StockSpanner"]

cases = [
    # LeetCode example
    ([100, 80, 60, 70, 60, 75, 85], [1, 1, 1, 2, 1, 4, 6]),
    # single call
    ([5], [1]),
    # strictly increasing
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    # strictly decreasing
    ([5, 4, 3, 2, 1], [1, 1, 1, 1, 1]),
    # all equal
    ([3, 3, 3, 3], [1, 2, 3, 4]),
    # statement example 1: [7, 2, 1, 2] then 2
    ([7, 2, 1, 2, 2], [1, 1, 1, 3, 4]),
    # statement example 2: [7, 34, 1, 2] then 8
    ([7, 34, 1, 2, 8], [1, 2, 1, 2, 3]),
    # alternating low/high
    ([1, 5, 1, 5, 1, 5], [1, 2, 1, 4, 1, 6]),
    # classic mixed
    ([10, 4, 5, 90, 120, 80], [1, 1, 2, 4, 5, 1]),
    # plateau then dip then plateau value
    ([2, 2, 1, 2], [1, 2, 1, 4]),
    # large: 10^4 equal prices (brute force is quadratic)
    ([100000] * 10000, list(range(1, 10001))),
    # large: descending then a max price swallowing everything
    ([100000 - i for i in range(9999)] + [100000], [1] * 9999 + [10000]),
]


def run(prices):
    s = StockSpanner()
    return [s.next(p) for p in prices]


def show(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for n, (prices, expected) in enumerate(cases, 1):
    try:
        got = run(prices)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={show(prices)}, expected={show(expected)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={show(prices)}, expected={show(expected)}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)