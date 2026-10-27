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


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_graph(adj):
    """Build graph from 1-based adjacency list; return (root, all_nodes)."""
    if not adj:
        return None, []
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nbrs]
    return nodes[0], nodes


def serialize_graph(root):
    """Return (adjacency list with sorted neighbors, nodes list); raises on inconsistent val->object mapping."""
    if root is None:
        return [], []
    by_val = {}
    seen = set()
    stack = [root]
    while stack:
        cur = stack.pop()
        if id(cur) in seen:
            continue
        seen.add(id(cur))
        if cur.val in by_val and by_val[cur.val] is not cur:
            raise ValueError(f"multiple distinct node objects with val={cur.val}")
        by_val[cur.val] = cur
        for nb in cur.neighbors:
            stack.append(nb)
    n = max(by_val)
    adj = []
    for v in range(1, n + 1):
        if v not in by_val:
            adj.append(None)
        else:
            adj.append(sorted(nb.val for nb in by_val[v].neighbors))
    return adj, list(by_val.values())


def canon(adj):
    return [sorted(x) for x in adj]


def cycle(n):
    if n == 1:
        return [[]]
    if n == 2:
        return [[2], [1]]
    return [sorted([(i - 1) % n + 1, (i + 1) % n + 1]) for i in range(n)]


def path(n):
    adj = []
    for i in range(1, n + 1):
        nb = []
        if i > 1:
            nb.append(i - 1)
        if i < n:
            nb.append(i + 1)
        adj.append(nb)
    return adj


def complete(n):
    return [[j for j in range(1, n + 1) if j != i] for i in range(1, n + 1)]


def star(n):
    adj = [list(range(2, n + 1))]
    for _ in range(2, n + 1):
        adj.append([1])
    return adj


CASES = [
    ("example 1: 4-cycle", [[2, 4], [1, 3], [2, 4], [1, 3]]),
    ("example 2: single node", [[]]),
    ("example 3: empty graph", []),
    ("two nodes", [[2], [1]]),
    ("triangle", [[2, 3], [1, 3], [1, 2]]),
    ("path of 5", path(5)),
    ("star of 7", star(7)),
    ("complete graph K6", complete(6)),
    ("triangle with tail", [[2, 3], [1, 3], [1, 2, 4], [3, 5], [4]]),
    ("cycle of 100", cycle(100)),
    ("path of 100", path(100)),
    ("complete graph K30", complete(30)),
]


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional,
      "Dict": Dict, "Node": Node}
exec(open("attempt.py").read(), ns)


def run_case(adj):
    root, nodes = build_graph(adj)
    original_ids = {id(n) for n in nodes}
    sol = ns["Solution"]()
    result = sol.cloneGraph(root)

    if not adj:
        return result is None, ("None" if result is None else "non-None"), [], None

    if result is None:
        return False, "None", adj, None
    if id(result) in original_ids:
        return False, "returned original node", adj, None
    got_adj, got_nodes = serialize_graph(result)
    if any(id(n) in original_ids for n in got_nodes):
        return False, "clone shares nodes with original", adj, None
    # original must be unchanged
    orig_adj, _ = serialize_graph(root)
    if orig_adj != canon(adj):
        return False, "original graph was modified", adj, None
    return got_adj == canon(adj), got_adj, canon(adj), None


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


passed = 0
total = len(CASES)
for i, (name, adj) in enumerate(CASES, 1):
    try:
        ok, got, expected, _ = run_case(adj)
        if ok:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={short(adj)}, expected={short(expected)}, got={short(got)}  ({name})")
    except Exception as e:
        print(f"FAIL case {i}: input={short(adj)}, error={type(e).__name__}: {e}  ({name})")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)