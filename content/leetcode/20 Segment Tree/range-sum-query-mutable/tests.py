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


def list_to_py(node):
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


def tree_to_list(root):
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
NumArray = ns["NumArray"]


def run(ops, args):
    obj = None
    res = []
    for op, a in zip(ops, args):
        if op == "NumArray":
            obj = NumArray(list(a[0]))
            res.append(None)
        elif op == "update":
            obj.update(*a)
            res.append(None)
        else:
            res.append(obj.sumRange(*a))
    return res


def mk(nums, steps):
    """steps: list of (op, args, expected)."""
    ops = ["NumArray"] + [s[0] for s in steps]
    args = [[nums]] + [list(s[1]) for s in steps]
    exp = [None] + [s[2] for s in steps]
    return ops, args, exp


S = "sumRange"
U = "update"

cases = []

# 1: example
cases.append(mk([1, 3, 5], [(S, (0, 2), 9), (U, (1, 2), None), (S, (0, 2), 8)]))

# 2: single element
cases.append(mk([5], [(S, (0, 0), 5), (U, (0, 0), None), (S, (0, 0), -3)]))
cases[-1][2][-1] = -3
cases[-1][1][2] = [0, -3]

# 3: negatives
cases.append(mk([-1, -2, -3, -4], [
    (S, (0, 3), -10), (S, (1, 2), -5), (U, (2, 3), None), (S, (1, 2), 1), (S, (0, 3), -4)]))

# 4: odd length
cases.append(mk([1, 2, 3, 4, 5], [
    (S, (0, 4), 15), (S, (2, 2), 3), (U, (4, -5), None), (S, (3, 4), -1), (S, (0, 4), 5)]))

# 5: length 8, updates at ends
cases.append(mk([1, 2, 3, 4, 5, 6, 7, 8], [
    (S, (0, 7), 36), (S, (3, 6), 22), (U, (7, 0), None), (S, (0, 7), 28),
    (S, (6, 7), 7), (U, (0, 10), None), (S, (0, 2), 15)]))

# 6: two elements
cases.append(mk([0, 0], [
    (S, (0, 1), 0), (U, (0, 100), None), (S, (0, 1), 100),
    (U, (1, -100), None), (S, (0, 1), 0), (S, (1, 1), -100)]))

# 7: repeated identical updates
cases.append(mk([7, 7, 7], [
    (U, (1, 7), None), (S, (0, 2), 21), (U, (1, 7), None), (S, (1, 1), 7)]))

# 8: power of two length
cases.append(mk([10, 20, 30, 40], [
    (S, (1, 3), 90), (U, (0, -10), None), (S, (0, 1), 10), (S, (0, 3), 80)]))

# 9: boundary values
cases.append(mk([100, -100, 100, -100, 100, -100], [
    (S, (0, 5), 0), (S, (0, 0), 100), (S, (5, 5), -100),
    (U, (5, 100), None), (S, (0, 5), 200), (S, (4, 5), 200)]))

# 10: non power of two length 7
cases.append(mk([3, 1, 4, 1, 5, 9, 2], [
    (S, (0, 6), 25), (S, (2, 4), 10), (U, (3, -1), None),
    (S, (2, 4), 8), (S, (1, 5), 18), (S, (0, 6), 23)]))

# 11: large input
big_steps = [
    (S, (0, 29999), 30000),
    (U, (15000, 100), None),
    (S, (0, 29999), 30099),
    (S, (15000, 15000), 100),
    (S, (10000, 19999), 10099),
]
for i in range(15000):
    big_steps.append((U, (i, 2), None))
big_steps += [
    (S, (0, 14999), 30000),
    (S, (15000, 29999), 15099),
    (S, (0, 29999), 45099),
]
cases.append(mk([1] * 30000, big_steps))


def short(x):
    s = repr(x)
    return s if len(s) < 300 else s[:300] + "..."


passed = 0
for n, (ops, args, exp) in enumerate(cases, 1):
    try:
        got = run(ops, args)
    except Exception as e:
        print(f"FAIL case {n}: input={short((ops, args))}, expected={short(exp)}, got=Exception: {e}")
        continue
    if got == exp:
        passed += 1
        print(f"PASS case {n}")
    else:
        idx = next((i for i in range(min(len(got), len(exp))) if got[i] != exp[i]), None)
        print(f"FAIL case {n}: input={short((ops, args))}, expected={short(exp)}, got={short(got)} first mismatch at op {idx}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
