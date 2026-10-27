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
    q = [root]
    i = 1
    while q and i < len(vals):
        n = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i])
            q.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i])
            q.append(n.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def reference(intervals, new):
    res = []
    for s, e in intervals:
        if e < new[0]:
            res.append([s, e])
        elif s > new[1]:
            res.append(list(new))
            new = [s, e]
        else:
            new = [min(new[0], s), max(new[1], e)]
    res.append(list(new))
    return res


def norm(x):
    return [list(p) for p in x]


big = [[2 * i, 2 * i] for i in range(5000)]
big_touch = [[3 * i, 3 * i + 1] for i in range(3333)]

cases = [
    ([[1, 3], [6, 9]], [2, 5], [[1, 5], [6, 9]]),
    ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8], [[1, 2], [3, 10], [12, 16]]),
    ([], [5, 7], [[5, 7]]),
    ([[1, 5]], [2, 3], [[1, 5]]),
    ([[1, 5]], [6, 8], [[1, 5], [6, 8]]),
    ([[3, 5]], [0, 1], [[0, 1], [3, 5]]),
    ([[1, 2], [3, 4]], [2, 3], [[1, 4]]),
    ([[1, 2], [5, 6]], [3, 4], [[1, 2], [3, 4], [5, 6]]),
    ([[1, 2], [3, 4], [5, 6]], [0, 100000], [[0, 100000]]),
    ([[0, 0], [2, 2]], [1, 1], [[0, 0], [1, 1], [2, 2]]),
    ([[1, 2], [3, 4]], [5, 5], [[1, 2], [3, 4], [5, 5]]),
    ([[1, 2], [4, 5]], [2, 4], [[1, 5]]),
    (big, [5000, 5001], None),
    (big_touch, [100, 5000], None),
]

passed = 0
total = len(cases)
for n, (intervals, new, exp) in enumerate(cases, 1):
    if exp is None:
        exp = reference(intervals, new)
    inp_a = copy.deepcopy(intervals)
    inp_b = list(new)
    short = f"intervals={intervals}, newInterval={new}"
    if len(short) > 200:
        short = f"intervals(len={len(intervals)}), newInterval={new}"
    try:
        got = ns["Solution"]().insert(inp_a, inp_b)
        if norm(got) == norm(exp):
            print(f"PASS case {n}")
            passed += 1
        else:
            g = str(got)
            e = str(exp)
            if len(g) > 200:
                g = g[:200] + "..."
            if len(e) > 200:
                e = e[:200] + "..."
            print(f"FAIL case {n}: input={short}, expected={e}, got={g}")
    except Exception as ex:
        print(f"FAIL case {n}: input={short}, error={type(ex).__name__}: {ex}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
