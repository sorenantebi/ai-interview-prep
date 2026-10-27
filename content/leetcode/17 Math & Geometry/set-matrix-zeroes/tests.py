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


def brute(matrix):
    rows, cols = len(matrix), len(matrix[0])
    zr = {r for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    zc = {c for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    return [[0 if (r in zr or c in zc) else matrix[r][c] for c in range(cols)]
            for r in range(rows)]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
      "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def make_random(seed, rows, cols, zero_prob):
    import random
    rng = random.Random(seed)
    return [[0 if rng.random() < zero_prob else rng.choice([-5, -1, 1, 2, 7, 2**31 - 1, -2**31])
             for _ in range(cols)] for _ in range(rows)]


big_empty = [[1] * 200 for _ in range(200)]
big_empty[100][150] = 0
big_corner = [[3] * 200 for _ in range(200)]
big_corner[199][199] = 0

cases = [
    ([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
    ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
    ([[0]], [[0]]),
    ([[5]], [[5]]),
    ([[1, 0, 3]], [[0, 0, 0]]),
    ([[1], [0], [3]], [[0], [0], [0]]),
    ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
    ([[0, 0], [0, 0]], [[0, 0], [0, 0]]),
    ([[0, 1, 2], [3, 4, 5], [6, 7, 8]], [[0, 0, 0], [0, 4, 5], [0, 7, 8]]),
    ([[1, 2, 0], [3, 4, 5], [6, 7, 8]], [[0, 0, 0], [3, 4, 0], [6, 7, 0]]),
    ([[1, 2, 3], [0, 4, 5], [6, 7, 8]], [[0, 2, 3], [0, 0, 0], [0, 7, 8]]),
    ([[-2**31, 0, 2**31 - 1], [-1, 5, -7], [0, 3, 4]],
     [[0, 0, 0], [0, 0, -7], [0, 0, 0]]),
    ([[1, 0, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1]],
     [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    (make_random(1, 7, 5, 0.1), None),
    (make_random(2, 30, 40, 0.02), None),
    (big_empty, None),
    (big_corner, None),
]

passed = 0
total = len(cases)
for i, (inp, exp) in enumerate(cases, 1):
    original = copy.deepcopy(inp)
    if exp is None:
        exp = brute(original)
    work = copy.deepcopy(inp)
    shown = original if len(original) * len(original[0]) <= 50 else f"<{len(original)}x{len(original[0])} matrix>"
    try:
        ns["Solution"]().setZeroes(work)
        if work == exp:
            passed += 1
            print(f"PASS case {i}")
        else:
            got = work if len(work) * len(work[0]) <= 50 else f"<{len(work)}x{len(work[0])} matrix>"
            exp_s = exp if len(exp) * len(exp[0]) <= 50 else f"<{len(exp)}x{len(exp[0])} matrix>"
            print(f"FAIL case {i}: input={shown}, expected={exp_s}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)