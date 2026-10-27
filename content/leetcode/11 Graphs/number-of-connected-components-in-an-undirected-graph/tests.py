import sys
import random
from typing import List, Optional, Dict

sys.setrecursionlimit(20000)


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


def brute(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    count = 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        stack = [s]
        seen[s] = True
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return count


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

rng = random.Random(12345)

# random sparse graph
n_sparse = 2000
sparse_edges = set()
while len(sparse_edges) < 800:
    a, b = rng.randrange(n_sparse), rng.randrange(n_sparse)
    if a != b and (a, b) not in sparse_edges and (b, a) not in sparse_edges:
        sparse_edges.add((a, b))
sparse_edges = [list(e) for e in sparse_edges]

# random dense graph
n_dense = 2000
dense_edges = set()
while len(dense_edges) < 5000:
    a, b = rng.randrange(n_dense), rng.randrange(n_dense)
    if a != b and (a, b) not in dense_edges and (b, a) not in dense_edges:
        dense_edges.add((a, b))
dense_edges = [list(e) for e in dense_edges]

chain = [[i, i + 1] for i in range(1999)]

cases = [
    (5, [[0, 1], [1, 2], [3, 4]], 2),
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]], 1),
    (1, [], 1),
    (2, [[0, 1]], 1),
    (4, [[0, 1]], 3),
    (4, [[0, 1], [1, 2], [2, 0]], 2),
    (6, [[0, 1], [2, 3], [4, 5]], 3),
    (5, [[4, 3], [3, 2], [2, 1], [1, 0]], 1),
    (2000, [[0, i] for i in range(1, 2000)], 1),
    (2000, chain, 1),
    (2000, [list(reversed(e)) for e in reversed(chain)], 1),
    (n_sparse, sparse_edges, brute(n_sparse, sparse_edges)),
    (n_dense, dense_edges, brute(n_dense, dense_edges)),
    (2000, [[0, 1]], 1999),
]


def fmt(n, edges):
    if len(edges) > 10:
        return f"n={n}, edges=<{len(edges)} edges>"
    return f"n={n}, edges={edges}"


passed = 0
total = len(cases)
for i, (n, edges, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.countComponents(n, [list(e) for e in edges])
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={fmt(n, edges)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={fmt(n, edges)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
