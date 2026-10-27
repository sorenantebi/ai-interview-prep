import sys
import random
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


def reference(edges):
    par = list(range(len(edges) + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        par[ra] = rb
    return None


def random_case(n, seed):
    rnd = random.Random(seed)
    edges = set()
    for i in range(2, n + 1):
        edges.add((rnd.randint(1, i - 1), i))
    while len(edges) < n:
        a, b = sorted(rnd.sample(range(1, n + 1), 2))
        edges.add((a, b))
    lst = [list(e) for e in edges]
    rnd.shuffle(lst)
    return lst


path_1000 = [[i, i + 1] for i in range(1, 1000)] + [[1, 1000]]
path_1000_rev = [[1, 1000]] + [[i, i + 1] for i in range(1, 1000)]
star_1000 = [[1, i] for i in range(2, 1000)] + [[2, 3]]

cases = [
    ([[1, 2], [1, 3], [2, 3]], [2, 3]),
    ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], [1, 4]),
    ([[2, 3], [1, 3], [1, 2]], [1, 2]),
    ([[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]], [1, 5]),
    ([[1, 2], [1, 3], [2, 3], [3, 4], [4, 5]], [2, 3]),
    ([[1, 2], [1, 3], [1, 4], [3, 4]], [3, 4]),
    ([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]], [1, 3]),
    ([[1, 2], [2, 3], [3, 4], [4, 5], [2, 5], [5, 6]], [2, 5]),
    (path_1000, [1, 1000]),
    (path_1000_rev, reference(path_1000_rev)),
    (star_1000, [2, 3]),
    (random_case(1000, 1), None),
    (random_case(500, 2), None),
    (random_case(50, 3), None),
]
cases = [(e, exp if exp is not None else reference(e)) for e, exp in cases]


def run():
    sol = ns["Solution"]()
    passed = 0
    for i, (edges, expected) in enumerate(cases, 1):
        shown = edges if len(edges) <= 10 else f"<{len(edges)} edges>"
        try:
            got = sol.findRedundantConnection([list(e) for e in edges])
            ok = got is not None and list(got) == expected
        except Exception as ex:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got=exception {type(ex).__name__}: {ex}")
            continue
        if ok:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={shown}, expected={expected}, got={got}")
    print(f"{passed}/{len(cases)} passed")
    if passed != len(cases):
        sys.exit(1)


run()
