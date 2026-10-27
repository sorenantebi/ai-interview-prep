import sys
import heapq
import random
import collections
from collections import deque
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


def tree_to_py(root):
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "heapq": heapq,
    "collections": collections,
}
exec(open("attempt.py").read(), ns)


def oracle(grid):
    """Independent check: binary search on t + BFS."""
    n = len(grid)

    def reachable(t):
        if grid[0][0] > t:
            return False
        seen = {(0, 0)}
        q = deque([(0, 0)])
        while q:
            r, c = q.popleft()
            if (r, c) == (n - 1, n - 1):
                return True
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] <= t:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return False

    lo, hi = 0, n * n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if reachable(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def random_grid(n, seed):
    vals = list(range(n * n))
    random.Random(seed).shuffle(vals)
    return [vals[i * n:(i + 1) * n] for i in range(n)]


def row_major(n):
    return [[r * n + c for c in range(n)] for r in range(n)]


def snake(n):
    g = [[0] * n for _ in range(n)]
    k = 0
    for r in range(n):
        cols = range(n) if r % 2 == 0 else range(n - 1, -1, -1)
        for c in cols:
            g[r][c] = k
            k += 1
    return g


g5 = random_grid(5, 1)
g7 = random_grid(7, 2)
g50 = random_grid(50, 3)
gs50 = snake(50)

cases = [
    ([[0, 2], [1, 3]], 3),
    ([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
      [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]], 16),
    ([[0]], 0),
    ([[3, 2], [1, 0]], 3),
    ([[0, 1], [3, 2]], 2),
    ([[0, 3], [1, 2]], 2),
    ([[0, 1, 2], [3, 4, 5], [6, 7, 8]], 8),
    ([[8, 7, 6], [5, 4, 3], [2, 1, 0]], 8),
    ([[0, 8, 7], [1, 5, 6], [2, 3, 4]], 4),
    (g5, oracle(g5)),
    (g7, oracle(g7)),
    (row_major(50), 2499),
    (g50, oracle(g50)),
    (gs50, oracle(gs50)),
]

passed = 0
total = len(cases)
for i, (grid, expected) in enumerate(cases, 1):
    shown = grid if len(grid) <= 7 else "<%dx%d grid>" % (len(grid), len(grid))
    try:
        got = ns["Solution"]().swimInWater([row[:] for row in grid])
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
