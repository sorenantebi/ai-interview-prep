import sys
import heapq
import math
import random
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "heapq": heapq,
    "math": math,
}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def canon(res):
    return sorted(tuple(p) for p in res)


def brute(points, k):
    return canon(sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])[:k])


def tie_free_k(points, k):
    """Move k so that there is no distance tie at the boundary."""
    d = sorted(x * x + y * y for x, y in points)
    while k < len(points) and d[k - 1] == d[k]:
        k += 1
    return k


cases = []

# Examples
cases.append(([[1, 3], [-2, 2]], 1, [(-2, 2)]))
cases.append(([[3, 3], [5, -1], [-2, 4]], 2, [(-2, 4), (3, 3)]))

# Single point
cases.append(([[0, 0]], 1, [(0, 0)]))
cases.append(([[10000, -10000]], 1, [(10000, -10000)]))

# k == len(points)
cases.append(([[2, 2], [-1, 0], [0, 5]], 3, [(-1, 0), (0, 5), (2, 2)]))

# Negatives in all quadrants
cases.append(([[-1, -1], [4, 4], [-5, 5], [3, -3]], 2, [(-1, -1), (3, -3)]))

# Duplicate points
cases.append(([[1, 1], [1, 1], [2, 2], [3, 3]], 2, [(1, 1), (1, 1)]))

# Points on axes and origin
cases.append(([[0, 0], [0, 3], [-4, 0], [5, 0]], 3, [(-4, 0), (0, 0), (0, 3)]))

# Equal distance points inside the kept set (tie not at boundary)
cases.append(([[1, 0], [0, 1], [-1, 0], [0, -1], [9, 9]], 4,
              [(-1, 0), (0, -1), (0, 1), (1, 0)]))

# Extreme coordinates
cases.append(([[-10000, -10000], [10000, 10000], [1, 1], [-9999, 10000]], 1, [(1, 1)]))

# Large random inputs
rng = random.Random(12345)
pts = [[rng.randint(-10000, 10000), rng.randint(-10000, 10000)] for _ in range(10000)]
k = tie_free_k(pts, 100)
cases.append((pts, k, brute(pts, k)))

pts = [[rng.randint(-10000, 10000), rng.randint(-10000, 10000)] for _ in range(10000)]
k = tie_free_k(pts, 5000)
cases.append((pts, k, brute(pts, k)))

pts = [[rng.randint(-10000, 10000), rng.randint(-10000, 10000)] for _ in range(10000)]
cases.append((pts, 10000, brute(pts, 10000)))


def short(v):
    s = repr(v)
    return s if len(s) <= 200 else s[:200] + "...(%d chars)" % len(s)


passed = 0
for i, (points, k, expected) in enumerate(cases, 1):
    try:
        got = Solution().kClosest([list(p) for p in points], k)
        got_c = canon(got)
        if got_c == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({short(points)}, {k}), expected={short(expected)}, got={short(got_c)}")
    except Exception as e:
        print(f"FAIL case {i}: input=({short(points)}, {k}), error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)