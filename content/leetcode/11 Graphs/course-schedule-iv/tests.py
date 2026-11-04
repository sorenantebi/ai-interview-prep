import sys
import copy
from typing import List, Optional, Dict
from collections import defaultdict, deque


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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
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
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "defaultdict": defaultdict,
    "deque": deque,
}
exec(open("attempt.py").read(), ns)


# Large inputs (expected values derived from the structure: edges i->j for i<j
# means u is a prerequisite of v exactly when u < v).
def big_queries():
    qs = []
    exp = []
    for k in range(10000):
        u = k % 100
        v = (u + 1 + (k // 100) % 99) % 100
        qs.append([u, v])
        exp.append(u < v)
    return qs, exp


big_q, big_exp = big_queries()
chain100 = [[i, i + 1] for i in range(99)]
complete100 = [[i, j] for i in range(100) for j in range(i + 1, 100)]

cases = [
    # 1-3: examples
    (2, [[1, 0]], [[0, 1], [1, 0]], [False, True]),
    (2, [], [[1, 0], [0, 1]], [False, False]),
    (3, [[1, 2], [1, 0], [2, 0]], [[1, 0], [1, 2]], [True, True]),
    # 4: simple chain
    (5, [[0, 1], [1, 2], [2, 3], [3, 4]],
     [[0, 4], [4, 0], [1, 3], [3, 1], [2, 4]],
     [True, False, True, False, True]),
    # 5: diamond
    (4, [[0, 1], [0, 2], [1, 3], [2, 3]],
     [[0, 3], [1, 2], [2, 1], [3, 0], [0, 1]],
     [True, False, False, False, True]),
    # 6: disconnected components
    (5, [[0, 1], [2, 3]],
     [[0, 3], [2, 3], [1, 0], [4, 0], [0, 4]],
     [False, True, False, False, False]),
    # 7: minimal single query
    (2, [[0, 1]], [[0, 1]], [True]),
    # 8: repeated queries
    (3, [[0, 1], [1, 2]], [[0, 2], [0, 2], [2, 0], [2, 0]],
     [True, True, False, False]),
    # 9: reversed labels
    (4, [[3, 2], [2, 1], [1, 0]],
     [[3, 0], [0, 3], [2, 0], [1, 2]],
     [True, False, True, False]),
    # 10: branching tree
    (6, [[0, 1], [0, 2], [1, 3], [2, 4], [4, 5]],
     [[0, 5], [1, 5], [3, 5], [2, 5], [0, 3], [1, 4]],
     [True, False, False, True, True, False]),
    # 11: large chain, 10^4 queries
    (100, chain100, big_q, big_exp),
    # 12: large complete DAG, 4950 edges, 10^4 queries
    (100, complete100, big_q, big_exp),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
total = len(cases)
for i, (n, pre, qs, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.checkIfPrerequisite(n, copy.deepcopy(pre), copy.deepcopy(qs))
        got_norm = [bool(x) for x in got]
        if got_norm == expected and len(got) == len(expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short((n, pre, qs))}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short((n, pre, qs))}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)