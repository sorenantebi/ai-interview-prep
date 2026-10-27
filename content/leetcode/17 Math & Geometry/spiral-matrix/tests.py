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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def reference(matrix):
    m = [row[:] for row in matrix]
    res = []
    while m:
        res.extend(m.pop(0))
        m = [list(r) for r in zip(*m)][::-1]
    return res


def grid(m, n, start=1):
    return [[start + i * n + j for j in range(n)] for i in range(m)]


cases = [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
    ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
    ([[5]], [5]),
    ([[1, 2, 3, 4, 5]], [1, 2, 3, 4, 5]),
    ([[1], [2], [3], [4]], [1, 2, 3, 4]),
    ([[1, 2], [3, 4]], [1, 2, 4, 3]),
    ([[-1, -2, -3], [0, 0, 0], [100, -100, 50]], [-1, -2, -3, 0, 50, -100, 100, 0, 0]),
    (grid(4, 4), reference(grid(4, 4))),
    (grid(5, 2), [1, 2, 4, 6, 8, 10, 9, 7, 5, 3]),
    (grid(2, 5), [1, 2, 3, 4, 5, 10, 9, 8, 7, 6]),
    (grid(3, 1), [1, 4, 7][:0] + [1, 2, 3]),
    (grid(10, 10), reference(grid(10, 10))),
    (grid(1, 10), list(range(1, 11))),
    (grid(10, 3), reference(grid(10, 3))),
]

passed = 0
total = len(cases)
for idx, (matrix, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().spiralOrder(copy.deepcopy(matrix))
        if list(got) == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={matrix}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={matrix}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)