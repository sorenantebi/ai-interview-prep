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


class Node:
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "Node": Node,
      "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def canon(node):
    # leaf -> (1, val); internal -> (0, tl, tr, bl, br); val of internal nodes is ignored
    if node is None:
        return None
    if node.isLeaf:
        return (1, 1 if node.val else 0)
    return (0, canon(node.topLeft), canon(node.topRight),
            canon(node.bottomLeft), canon(node.bottomRight))


def count(node):
    if node is None:
        return 0
    return 1 + count(node.topLeft) + count(node.topRight) + count(node.bottomLeft) + count(node.bottomRight)


def uniform(grid, r, c, size):
    v = grid[r][c]
    for i in range(r, r + size):
        for j in range(c, c + size):
            if grid[i][j] != v:
                return False
    return True


def valid(node, grid, r, c, size):
    if node is None:
        return False
    kids = [node.topLeft, node.topRight, node.bottomLeft, node.bottomRight]
    if node.isLeaf:
        if any(k is not None for k in kids):
            return False
        return uniform(grid, r, c, size) and (1 if node.val else 0) == grid[r][c]
    if size == 1 or any(k is None for k in kids):
        return False
    if uniform(grid, r, c, size):
        return False
    h = size // 2
    return (valid(node.topLeft, grid, r, c, h)
            and valid(node.topRight, grid, r, c + h, h)
            and valid(node.bottomLeft, grid, r + h, c, h)
            and valid(node.bottomRight, grid, r + h, c + h, h))


L0 = (1, 0)
L1 = (1, 1)

ex2 = [
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
]

checker64 = [[(i + j) % 2 for j in range(64)] for i in range(64)]
ones64 = [[1] * 64 for _ in range(64)]
corner64 = [[0] * 64 for _ in range(64)]
corner64[63][63] = 1

# (grid, expected canonical form or None, expected node count or None)
cases = [
    ([[0, 1], [1, 0]], (0, L0, L1, L1, L0), 5),
    (ex2, (0, L1, (0, L0, L0, L1, L1), L1, L0), 9),
    ([[1]], L1, 1),
    ([[0]], L0, 1),
    ([[1, 1], [1, 1]], L1, 1),
    ([[0, 0], [0, 0]], L0, 1),
    ([[1] * 4 for _ in range(4)], L1, 1),
    ([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]], (0, L1, L0, L0, L1), 5),
    ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
     (0, (0, L1, L0, L0, L0), L0, L0, L0), 9),
    (checker64, None, 5461),
    (ones64, L1, 1),
    (corner64, None, 25),
]

passed = 0
total = len(cases)
for idx, (grid, exp, exp_count) in enumerate(cases, 1):
    try:
        root = ns["Solution"]().construct(copy.deepcopy(grid))
        got = canon(root)
        n = len(grid)
        ok = valid(root, grid, 0, 0, n)
        if ok and exp is not None and got != exp:
            ok = False
        if ok and exp_count is not None and count(root) != exp_count:
            ok = False
        if ok:
            passed += 1
            print(f"PASS case {idx}")
        else:
            shown = grid if n <= 8 else f"<{n}x{n} grid>"
            exp_show = exp if exp is not None else f"valid tree with {exp_count} nodes"
            got_show = got if n <= 8 else f"tree with {count(root)} nodes"
            print(f"FAIL case {idx}: input={shown}, expected={exp_show}, got={got_show}")
    except Exception as e:
        print(f"FAIL case {idx}: input=<grid>, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)