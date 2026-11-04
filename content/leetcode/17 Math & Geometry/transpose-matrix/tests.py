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
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

# Large inputs with structurally known expected outputs
big_row = [list(range(100000))]
big_row_exp = [[i] for i in range(100000)]
big_col = [[i] for i in range(100000)]
big_col_exp = [list(range(100000))]
sq = 316
big_sq = [[i * sq + j for j in range(sq)] for i in range(sq)]
big_sq_exp = [[j * sq + i for j in range(sq)] for i in range(sq)]
rect = [[i * 100 + j for j in range(100)] for i in range(1000)]
rect_exp = [[i * 100 + j for i in range(1000)] for j in range(100)]

cases = [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
    ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
    ([[5]], [[5]]),
    ([[1, 2, 3, 4]], [[1], [2], [3], [4]]),
    ([[1], [2], [3], [4]], [[1, 2, 3, 4]]),
    ([[-1, -2], [-3, -4], [-5, -6]], [[-1, -3, -5], [-2, -4, -6]]),
    ([[7, 7], [7, 7]], [[7, 7], [7, 7]]),
    ([[1000000000, -1000000000], [0, 5]], [[1000000000, 0], [-1000000000, 5]]),
    (big_row, big_row_exp),
    (big_col, big_col_exp),
    (big_sq, big_sq_exp),
    (rect, rect_exp),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for idx, (inp, exp) in enumerate(cases, 1):
    try:
        arg = [row[:] for row in inp]
        got = ns["Solution"]().transpose(arg)
        got_norm = [list(r) for r in got] if got is not None else got
        if got_norm == exp:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short(inp)}, expected={short(exp)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)