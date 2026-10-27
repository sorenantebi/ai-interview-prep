import sys
import random
import heapq
import bisect
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
      "Optional": Optional, "Dict": Dict, "heapq": heapq, "bisect": bisect}
exec(open("attempt.py").read(), ns)


def expected_medians(ops):
    data = []
    res = []
    for op in ops:
        if op[0] == "add":
            bisect.insort(data, op[1])
        else:
            n = len(data)
            if n % 2:
                res.append(float(data[n // 2]))
            else:
                res.append((data[n // 2 - 1] + data[n // 2]) / 2.0)
    return res


def adds(vals):
    return [("add", v) for v in vals]


def add_find(vals):
    ops = []
    for v in vals:
        ops.append(("add", v))
        ops.append(("find",))
    return ops


rng = random.Random(12345)

cases = []

# 1: Example 1
cases.append([("add", 1), ("add", 2), ("find",), ("add", 3), ("find",)])
# 2: Example 2
cases.append([("add", -1), ("find",), ("add", -2), ("find",)])
# 3: single element
cases.append([("add", 5), ("find",)])
# 4: single zero
cases.append([("add", 0), ("find",)])
# 5: all duplicates
cases.append(add_find([7] * 10))
# 6: two elements
cases.append([("add", 2), ("add", 3), ("find",)])
# 7: ascending
cases.append(add_find(list(range(1, 21))))
# 8: descending
cases.append(add_find(list(range(20, 0, -1))))
# 9: negatives and positives mixed
cases.append(add_find([-5, 10, -3, 0, 8, -100, 42, -1, 1, 0]))
# 10: extremes
cases.append(add_find([100000, -100000, 100000, -100000, 0]))
# 11: repeated find without add, then more adds
cases.append([("add", 4), ("find",), ("find",), ("add", 1), ("find",), ("find",),
              ("add", 9), ("find",), ("find",)])
# 12: values in [0, 100]
cases.append(add_find([rng.randint(0, 100) for _ in range(200)]))
# 13: many adds, then a find
cases.append(adds([rng.randint(-100000, 100000) for _ in range(500)]) + [("find",)])
# 14: large performance case
big = []
for i in range(25000):
    big.append(("add", rng.randint(-100000, 100000)))
    if i % 2 == 0:
        big.append(("find",))
cases.append(big)


def short(x, limit=300):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


def close(a, b):
    return len(a) == len(b) and all(abs(x - y) <= 1e-5 for x, y in zip(a, b))


passed = 0
total = len(cases)
for i, ops in enumerate(cases, 1):
    expected = expected_medians(ops)
    try:
        mf = ns["MedianFinder"]()
        got = []
        for op in ops:
            if op[0] == "add":
                mf.addNum(op[1])
            else:
                got.append(mf.findMedian())
        if close(got, expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(ops)}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(ops)}, expected={short(expected)}, got=Exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)