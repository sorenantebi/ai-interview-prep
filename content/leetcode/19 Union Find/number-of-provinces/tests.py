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


def mat(n, edges):
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 1
    for a, b in edges:
        m[a][b] = 1
        m[b][a] = 1
    return m


def blocks(n, size):
    edges = []
    for s in range(0, n, size):
        for i in range(s, s + size):
            for j in range(i + 1, s + size):
                edges.append((i, j))
    return mat(n, edges)


cases = [
    # (input matrix, expected)
    ([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),                         # example 1
    ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),                         # example 2
    ([[1]], 1),                                                     # single city
    ([[1, 1], [1, 1]], 1),                                          # two connected
    ([[1, 0], [0, 1]], 2),                                          # two isolated
    ([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]], 1),  # chain, indirect links
    (mat(5, [(0, 2), (3, 4)]), 3),                                  # {0,2},{1},{3,4}
    (mat(6, [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5)]), 1),          # star
    (mat(6, [(0, 5), (1, 4), (2, 3)]), 3),                          # three far-apart pairs
    (mat(200, []), 200),                                            # large, all isolated
    ([[1] * 200 for _ in range(200)], 1),                           # large, fully connected
    (blocks(200, 10), 20),                                          # large, 20 blocks of 10
    (mat(200, [(i, i + 1) for i in range(199)]), 1),                # large chain
    (mat(200, [(i, i + 1) for i in range(0, 199, 2)]), 100),        # large, 100 disjoint pairs
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for idx, (inp, expected) in enumerate(cases, 1):
    try:
        arg = [row[:] for row in inp]
        got = ns["Solution"]().findCircleNum(arg)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short(inp)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(inp)}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
