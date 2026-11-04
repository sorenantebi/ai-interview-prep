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

# Large inputs
N = 100000
star = [[0, i] for i in range(1, N)]
pairs = [[2 * i, 2 * i + 1] for i in range(N // 2)]
M = 99000
path_extra = [[i, i + 1] for i in range(M - 1)] + [[i, i + 2] for i in range(1000)]

cases = [
    # (n, connections, expected)
    (4, [[0, 1], [0, 2], [1, 2]], 1),
    (6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]], 2),
    (6, [[0, 1], [0, 2], [0, 3], [1, 2]], -1),
    (1, [], 0),
    (2, [[0, 1]], 0),
    (3, [[0, 1]], -1),
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0),
    (4, [[0, 1], [1, 2], [2, 0], [0, 3]], 0),
    (5, [[0, 1], [0, 2], [1, 2], [3, 4]], 1),
    (6, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]], 1),
    (N, star, 0),
    (N, pairs, -1),
    (N, path_extra, 1000),
]

passed = 0
total = len(cases)
for idx, (n, conns, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().makeConnected(n, [list(c) for c in conns])
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = conns if len(conns) <= 10 else f"<{len(conns)} connections>"
            print(f"FAIL case {idx}: input=(n={n}, connections={shown}), expected={expected}, got={got}")
    except Exception as e:
        shown = conns if len(conns) <= 10 else f"<{len(conns)} connections>"
        print(f"FAIL case {idx}: input=(n={n}, connections={shown}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
