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
        cur = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            cur.left = TreeNode(vals[i])
            queue.append(cur.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            cur.right = TreeNode(vals[i])
            queue.append(cur.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        cur = queue.pop(0)
        if cur is None:
            out.append(None)
        else:
            out.append(cur.val)
            queue.append(cur.left)
            queue.append(cur.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    # examples
    ([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]], 5),
    ([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]], 3),
    ([[0, 0]], 0),
    # two stones sharing a row
    ([[0, 0], [0, 1]], 1),
    # two stones sharing nothing
    ([[0, 0], [1, 1]], 0),
    # all in one row
    ([[0, 0], [0, 1], [0, 2], [0, 3]], 3),
    # all in one column
    ([[0, 5], [1, 5], [2, 5]], 2),
    # row index equals other stone's column index: must not be connected
    ([[0, 1], [1, 0]], 0),
    # extreme coordinates, one separate stone
    ([[10000, 10000], [10000, 0], [0, 10000], [5, 5]], 2),
    # two components
    ([[0, 0], [0, 1], [5, 5], [5, 6], [7, 6]], 3),
    # large: 1000 isolated diagonal stones
    ([[i, i] for i in range(1000)], 0),
    # large: one big cross-shaped component (999 stones)
    ([[i, 0] for i in range(500)] + [[0, j] for j in range(1, 500)], 998),
    # large: 30x30 grid, fully connected
    ([[i, j] for i in range(30) for j in range(30)], 899),
]

passed = 0
total = len(cases)
for idx, (stones, expected) in enumerate(cases, 1):
    try:
        inp = [list(s) for s in stones]
        got = ns["Solution"]().removeStones(inp)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            short = stones if len(stones) <= 10 else f"<{len(stones)} stones>"
            print(f"FAIL case {idx}: input={short}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)