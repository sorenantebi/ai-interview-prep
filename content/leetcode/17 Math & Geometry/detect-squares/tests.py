import sys
import random
from collections import Counter, defaultdict
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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "defaultdict": defaultdict,
    "Counter": Counter,
}
exec(open("attempt.py").read(), ns)
DetectSquares = ns["DetectSquares"]


def brute_expected(ops, maxd=1000):
    """Independent reference: returns expected outputs for count ops."""
    c = Counter()
    res = []
    for op, p in ops:
        if op == "add":
            c[(p[0], p[1])] += 1
        else:
            qx, qy = p
            total = 0
            for d in range(1, maxd + 1):
                for sx in (d, -d):
                    for sy in (d, -d):
                        x, y = qx + sx, qy + sy
                        total += c[(x, y)] * c[(x, qy)] * c[(qx, y)]
            # each square is counted once per diagonal direction (4 directions, distinct squares)
            res.append(total)
    return res


def run_ops(ops):
    ds = DetectSquares()
    out = []
    for op, p in ops:
        if op == "add":
            ds.add(list(p))
        else:
            out.append(ds.count(list(p)))
    return out


def A(x, y):
    return ("add", [x, y])


def C(x, y):
    return ("count", [x, y])


cases = []

# 1: example
cases.append((
    [A(3, 10), A(11, 2), A(3, 2), C(11, 10), C(14, 8), A(11, 2), C(11, 10)],
    [1, 0, 2],
))
# 2: empty structure
cases.append(([C(0, 0), C(1000, 1000)], [0, 0]))
# 3: single point, query same point
cases.append(([A(5, 5), C(5, 5)], [0]))
# 4: zero-area "square" from identical points
cases.append(([A(0, 0), A(0, 0), A(0, 0), C(0, 0)], [0]))
# 5: unit square at origin
cases.append(([A(0, 1), A(1, 0), A(1, 1), C(0, 0)], [1]))
# 6: boundary coordinates
cases.append(([A(1000, 0), A(0, 1000), A(0, 0), C(1000, 1000)], [1]))
# 7: rectangle, not a square
cases.append(([A(0, 0), A(0, 2), A(3, 0), C(3, 2)], [0]))
# 8: duplicate multiplicities
cases.append((
    [A(0, 1), A(0, 1), A(1, 0), A(1, 0), A(1, 0), A(1, 1), A(1, 1), C(0, 0)],
    [12],
))
# 9: two squares of different size on opposite sides of the query
cases.append((
    [A(1, 1), A(1, 2), A(2, 1), A(0, 0), A(0, 2), A(2, 0), C(2, 2)],
    [2],
))
# 10: count does not store the query point
cases.append((
    [A(0, 1), A(1, 0), C(1, 1), C(1, 1), A(0, 0), C(1, 1), C(1, 1)],
    [0, 0, 1, 1],
))
# 11: query point is itself stored (still counts squares through it)
cases.append((
    [A(2, 2), A(2, 5), A(5, 2), A(5, 5), C(2, 2), C(5, 5), C(2, 5), C(5, 2)],
    [1, 1, 1, 1],
))
# 12: four squares around the query (all directions)
cases.append((
    [A(0, 0), A(0, 1), A(1, 0), A(1, 1),
     A(2, 0), A(2, 1), A(0, 2), A(1, 2), A(2, 2), C(1, 1)],
    [4],
))


def make_random(seed, n_ops, rng_max, maxd):
    rnd = random.Random(seed)
    ops = []
    for _ in range(n_ops):
        p = [rnd.randint(0, rng_max), rnd.randint(0, rng_max)]
        ops.append(("add" if rnd.random() < 0.5 else "count", p))
    return ops, brute_expected(ops, maxd)


# 13: random small grid with many duplicates
ops13, exp13 = make_random(1, 1000, 6, 6)
cases.append((ops13, exp13))

# 14: performance, 3000 ops on a modest grid
ops14, exp14 = make_random(2, 3000, 30, 30)
cases.append((ops14, exp14))

# 15: many copies of the same points (large products)
ops15 = [A(0, 0)] * 700 + [A(0, 7)] * 700 + [A(7, 0)] * 700 + [C(7, 7)]
cases.append((ops15, [700 ** 3]))


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


passed = 0
for i, (ops, expected) in enumerate(cases, 1):
    try:
        got = run_ops(ops)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(ops)}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(ops)}, error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
