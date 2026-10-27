import sys
import random
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
    "deque": deque,
}
exec(open("attempt.py").read(), ns)

INF = 2147483647


def reference(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    q = deque((r, c) for r in range(R) for c in range(C) if g[r][c] == 0)
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == INF:
                g[nr][nc] = g[r][c] + 1
                q.append((nr, nc))
    return g


def short(x):
    s = repr(x)
    return s if len(s) <= 300 else s[:300] + "...(truncated)"


random.seed(12345)


def random_grid(R, C, pw, pg):
    g = []
    for _ in range(R):
        row = []
        for _ in range(C):
            x = random.random()
            row.append(-1 if x < pw else (0 if x < pw + pg else INF))
        g.append(row)
    return g


big_open = [[INF] * 250 for _ in range(250)]
big_open[0][0] = 0

big_snake = [[INF] * 250 for _ in range(250)]
for r in range(1, 250, 2):
    for c in range(250):
        big_snake[r][c] = -1
    if (r // 2) % 2 == 0:
        big_snake[r][249] = INF
    else:
        big_snake[r][0] = INF
big_snake[0][0] = 0

inputs = [
    # 1-3: examples
    [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]],
    [[-1]],
    [[INF, -1], [-1, 0]],
    # 4: single gate
    [[0]],
    # 5: single empty room, no gate
    [[INF]],
    # 6: no gates at all
    [[INF, INF, INF], [INF, -1, INF]],
    # 7: single row
    [[INF, INF, 0, INF, -1, INF, 0, INF, INF]],
    # 8: single column
    [[0], [INF], [INF], [-1], [INF], [0]],
    # 9: all gates and walls
    [[0, -1, 0], [-1, 0, -1]],
    # 10: random small
    random_grid(8, 8, 0.25, 0.1),
    # 11: random medium with many walls
    random_grid(20, 15, 0.4, 0.05),
    # 12: large open grid
    big_open,
    # 13: large snake path (long distances)
    big_snake,
]

passed = 0
total = len(inputs)
for i, grid in enumerate(inputs, 1):
    expected = reference(grid)
    work = [row[:] for row in grid]
    try:
        sol = ns["Solution"]()
        ret = sol.walls_and_gates(work)
        if work == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(grid)}, expected={short(expected)}, got={short(work)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(grid)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)