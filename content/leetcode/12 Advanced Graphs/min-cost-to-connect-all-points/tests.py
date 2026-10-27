import sys
import heapq
import collections
import math
import random
import itertools
import bisect
import functools
from typing import List, Optional, Dict, Tuple, Set
from collections import defaultdict, deque, Counter


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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
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
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def reference_mst(points):
    """Independent O(n^2) array-based Prim used to compute expected values."""
    n = len(points)
    INF = float("inf")
    dist = [INF] * n
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        used[u] = True
        total += best
        ux, uy = points[u]
        for j in range(n):
            if not used[j]:
                d = abs(ux - points[j][0]) + abs(uy - points[j][1])
                if d < dist[j]:
                    dist[j] = d
    return total


def random_points(n, lo, hi, seed):
    rng = random.Random(seed)
    seen = set()
    pts = []
    while len(pts) < n:
        p = (rng.randint(lo, hi), rng.randint(lo, hi))
        if p not in seen:
            seen.add(p)
            pts.append([p[0], p[1]])
    return pts


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "Tuple": Tuple,
    "Set": Set,
    "heapq": heapq,
    "collections": collections,
    "defaultdict": defaultdict,
    "deque": deque,
    "Counter": Counter,
    "math": math,
    "itertools": itertools,
    "bisect": bisect,
    "functools": functools,
}
exec(open("attempt.py").read(), ns)


def run(points):
    return ns["Solution"]().minCostConnectPoints([list(p) for p in points])


def describe(points):
    if len(points) > 20:
        return f"<{len(points)} points>"
    return str(points)


cases = []

# Examples
cases.append(([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]], 20))
cases.append(([[3, 12], [-2, 5], [-4, 1]], 18))
cases.append(([[0, 0]], 0))

# Edge cases
cases.append(([[0, 0], [1, 1]], 2))
cases.append(([[0, 0], [1, 0], [2, 0], [3, 0]], 3))
cases.append(([[0, 0], [0, 1], [1, 0], [1, 1]], 3))
cases.append(([[-1000000, -1000000], [1000000, 1000000]], 4000000))

# Collinear line of 100 points
line100 = [[i, 0] for i in range(100)]
cases.append((line100, 99))

# Random small / medium (expected computed by independent Prim)
p30 = random_points(30, -50, 50, 1)
cases.append((p30, reference_mst(p30)))
p200 = random_points(200, -1000000, 1000000, 2)
cases.append((p200, reference_mst(p200)))

# Large inputs for performance
p1000 = random_points(1000, -1000000, 1000000, 3)
cases.append((p1000, reference_mst(p1000)))
line1000 = [[0, i] for i in range(1000)]
cases.append((line1000, 999))

passed = 0
total = len(cases)
for idx, (points, expected) in enumerate(cases, 1):
    try:
        got = run(points)
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input={describe(points)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={describe(points)}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)