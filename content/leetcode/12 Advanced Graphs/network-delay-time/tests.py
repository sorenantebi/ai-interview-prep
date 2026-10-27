import sys
import random
import collections
import heapq
import math
import itertools
import functools
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
    q = collections.deque([root])
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
    out = []
    q = collections.deque([root])
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


def reference(times, n, k):
    # Bellman-Ford, independent of the attempt
    dist = [math.inf] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    best = max(dist[1:])
    return -1 if best == math.inf else best


def random_graph(n, m, seed, max_w=100):
    rng = random.Random(seed)
    pairs = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
    rng.shuffle(pairs)
    return [[u, v, rng.randint(0, max_w)] for u, v in pairs[:m]]


chain100 = [[i, i + 1, 100] for i in range(1, 100)]
star = [[3, i, i] for i in (1, 2, 4, 5, 6)]
dense = random_graph(100, 6000, 1)
sparse_rand = random_graph(100, 150, 2)
small_rand = random_graph(10, 30, 3, 20)

# (times, n, k, expected)
cases = [
    ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, 2),
    ([[1, 2, 1]], 2, 1, 1),
    ([[1, 2, 1]], 2, 2, -1),
    ([], 1, 1, 0),
    ([[1, 2, 0], [2, 3, 0]], 3, 1, 0),
    ([[1, 2, 10], [1, 3, 1], [3, 2, 1]], 3, 1, 2),
    ([[1, 2, 1], [3, 4, 1]], 4, 1, -1),
    (chain100, 100, 1, 9900),
    (chain100, 100, 50, -1),
    ([[1, 2, 1], [2, 3, 2], [3, 1, 3]], 3, 2, 5),
    ([[1, 2, 1], [1, 3, 4], [2, 3, 1], [3, 4, 1]], 4, 1, 3),
    (star, 6, 3, 6),
    ([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 5, 2, -1),
    (dense, 100, 1, reference(dense, 100, 1)),
    (sparse_rand, 100, 7, reference(sparse_rand, 100, 7)),
    (small_rand, 10, 4, reference(small_rand, 10, 4)),
]

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict,
      "collections": collections, "heapq": heapq, "math": math, "itertools": itertools,
      "functools": functools, "bisect": bisect}
exec(open("attempt.py").read(), ns)


def short(x, limit=120):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


passed = 0
total = len(cases)
for i, (times, n, k, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().networkDelayTime([list(e) for e in times], n, k)
    except Exception as e:
        print(f"FAIL case {i}: input=times={short(times)}, n={n}, k={k}, expected={expected}, got=exception: {type(e).__name__}: {e}")
        continue
    if got == expected:
        passed += 1
        print(f"PASS case {i}")
    else:
        print(f"FAIL case {i}: input=times={short(times)}, n={n}, k={k}, expected={expected}, got={got}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
