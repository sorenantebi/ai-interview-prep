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
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


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


sys.setrecursionlimit(20000)

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def snake(rows, cols):
    grid = [[0] * cols for _ in range(rows)]
    k = 0
    for r in range(rows):
        rng = range(cols) if r % 2 == 0 else range(cols - 1, -1, -1)
        for c in rng:
            grid[r][c] = k
            k += 1
    return grid


BIG = 2**31 - 1

cases = [
    ([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4),
    ([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4),
    ([[1]], 1),
    ([[0]], 1),
    ([[1, 2, 3]], 3),
    ([[3], [2], [1]], 3),
    ([[1, 1], [1, 1]], 1),
    ([[1, 2, 3], [8, 9, 4], [7, 6, 5]], 9),
    ([[7, 8, 9], [9, 7, 6], [7, 2, 3]], 6),
    ([[0, BIG], [BIG, 0]], 2),
    ([[1, 2], [4, 3]], 4),
    (snake(60, 60), 3600),
    ([[r * 200 + c for c in range(200)] for r in range(200)], 399),
    ([[5] * 200 for _ in range(200)], 1),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for i, (matrix, expected) in enumerate(cases, 1):
    try:
        arg = [row[:] for row in matrix]
        got = ns["Solution"]().longestIncreasingPath(arg)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(matrix)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(matrix)}, expected={expected}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)