import sys
import copy
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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
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
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


# Independent iterative reference used to derive expected values for large grids
def brute(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    best = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == 1:
                g[r][c] = 0
                stack = [(r, c)]
                cnt = 0
                while stack:
                    x, y = stack.pop()
                    cnt += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1:
                            g[nx][ny] = 0
                            stack.append((nx, ny))
                best = max(best, cnt)
    return best


def snake(n):
    g = []
    for i in range(n):
        if i % 2 == 0:
            g.append([1] * n)
        elif (i // 2) % 2 == 0:
            g.append([0] * (n - 1) + [1])
        else:
            g.append([1] + [0] * (n - 1))
    return g


def spiral_free_checker(n):
    return [[(r + c) % 2 for c in range(n)] for r in range(n)]


big_snake = snake(50)
big_full = [[1] * 50 for _ in range(50)]
big_zero = [[0] * 50 for _ in range(50)]
big_checker = spiral_free_checker(50)
ring = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]

cases = [
    ([[0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]], 4),
    ([[0, 0, 0, 0, 0, 0, 0, 0]], 0),
    ([[1]], 1),
    ([[0]], 0),
    ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 9),
    ([[1, 0], [0, 1]], 1),
    ([[1, 1, 0, 1, 1, 1, 0, 1]], 3),
    ([[1], [1], [0], [1], [1], [1]], 3),
    (ring, 16 + 1 if False else 16),
    ([[1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 0], [1, 1, 1]], 5),
    (big_checker, 1),
    (big_zero, 0),
    (big_snake, brute(big_snake)),
    (big_full, 2500),
]

# Deep recursion is legitimate for DFS on a 50x50 grid (up to 2500 frames)
sys.setrecursionlimit(20000)

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def short(g):
    s = repr(g)
    return s if len(s) < 200 else s[:200] + "...(%dx%d)" % (len(g), len(g[0]))


passed = 0
for i, (grid, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().maxAreaOfIsland(copy.deepcopy(grid))
    except BaseException as e:
        print(f"FAIL case {i}: input={short(grid)}, expected={expected}, got=error: {type(e).__name__}: {e}")
        continue
    if got == expected:
        print(f"PASS case {i}")
        passed += 1
    else:
        print(f"FAIL case {i}: input={short(grid)}, expected={expected}, got={got}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)