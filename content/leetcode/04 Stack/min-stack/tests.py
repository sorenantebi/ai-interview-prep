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


def model(ops, args):
    """Naive reference: recomputes min over the whole stack."""
    res = []
    st = []
    for op, a in zip(ops, args):
        if op == "MinStack":
            st = []
            res.append(None)
        elif op == "push":
            st.append(a[0])
            res.append(None)
        elif op == "pop":
            st.pop()
            res.append(None)
        elif op == "top":
            res.append(st[-1])
        elif op == "getMin":
            res.append(min(st))
    return res


def run(ops, args):
    res = []
    obj = None
    for op, a in zip(ops, args):
        if op == "MinStack":
            obj = ns["MinStack"](*a)
            res.append(None)
        else:
            res.append(getattr(obj, op)(*a))
    return res


def case(ops, args):
    return (ops, args, model(ops, args))


cases = []

# 1-2: examples from the problem statement (expected hardcoded)
cases.append((
    ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
    [[], [-2], [0], [-3], [], [], [], []],
    [None, None, None, None, -3, None, 0, -2],
))
cases.append((
    ["MinStack", "push", "push", "getMin", "pop", "getMin"],
    [[], [1], [1], [], [], []],
    [None, None, None, 1, None, 1],
))

# 3: single element
cases.append(case(["MinStack", "push", "top", "getMin"], [[], [42], [], []]))

# 4: single element, pop then push again
cases.append(case(
    ["MinStack", "push", "pop", "push", "getMin", "top"],
    [[], [5], [], [3], [], []],
))

# 5: strictly decreasing pushes
cases.append(case(
    ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
    [[], [3], [2], [1], [], [], [], [], []],
))

# 6: strictly increasing pushes
cases.append(case(
    ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin", "top"],
    [[], [1], [2], [3], [], [], [], [], [], []],
))

# 7: many duplicates of the minimum
cases.append(case(
    ["MinStack", "push", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin", "pop", "getMin", "top"],
    [[], [2], [1], [1], [1], [], [], [], [], [], [], [], []],
))

# 8: extreme values (32-bit bounds)
cases.append(case(
    ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin", "top"],
    [[], [2 ** 31 - 1], [-2 ** 31], [0], [], [], [], [], [], []],
))

# 9: all negatives
cases.append(case(
    ["MinStack", "push", "push", "push", "getMin", "top", "pop", "getMin", "top"],
    [[], [-5], [-10], [-7], [], [], [], [], []],
))

# 10: min removed, then min of the remainder (top is 5 after two pops)
cases.append(case(
    ["MinStack", "push", "push", "push", "push", "getMin", "pop", "pop", "getMin", "top"],
    [[], [0], [5], [-1], [7], [], [], [], [], []],
))

# 11: interleaved operations with repeated min changes
cases.append(case(
    ["MinStack", "push", "getMin", "push", "getMin", "push", "getMin", "pop", "getMin",
     "pop", "getMin", "push", "getMin", "top"],
    [[], [10], [], [-3], [], [-3], [], [], [], [], [], [-8], [], []],
))

# 12: large input for performance (random values, ~12000 calls)
rng = random.Random(12345)
ops = ["MinStack"]
args = [[]]
for _ in range(8000):
    ops.append("push")
    args.append([rng.randint(-2 ** 31, 2 ** 31 - 1)])
for _ in range(2000):
    ops.extend(["getMin", "top", "pop"])
    args.extend([[], [], []])
cases.append(case(ops, args))

# 13: large input, monotonic decreasing then fully drained
ops = ["MinStack"]
args = [[]]
for v in range(10000, 0, -1):
    ops.append("push")
    args.append([v])
for _ in range(5000):
    ops.extend(["getMin", "pop"])
    args.extend([[], []])
cases.append(case(ops, args))


def short(x):
    s = repr(x)
    return s if len(s) <= 300 else s[:300] + "..."


passed = 0
total = len(cases)
for i, (ops, args, expected) in enumerate(cases, 1):
    try:
        got = run(ops, args)
    except Exception as e:
        print(f"FAIL case {i}: input={short((ops, args))}, expected={short(expected)}, got=Exception: {e!r}")
        continue
    if got == expected:
        passed += 1
        print(f"PASS case {i}")
    else:
        print(f"FAIL case {i}: input={short((ops, args))}, expected={short(expected)}, got={short(got)}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)