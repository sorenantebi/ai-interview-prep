import sys
import random
from collections import deque
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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        n = q.popleft()
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
    out = []
    q = deque([root])
    while q:
        n = q.popleft()
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


def model_run(k, steps):
    """Independent model; steps is a list of (op, arg or None). Returns ops, args, expected."""
    d = deque()
    ops = ["MyCircularQueue"]
    args = [[k]]
    exp = [None]
    for op, a in steps:
        ops.append(op)
        if op == "enQueue":
            args.append([a])
            if len(d) == k:
                exp.append(False)
            else:
                d.append(a)
                exp.append(True)
        else:
            args.append([])
            if op == "deQueue":
                if d:
                    d.popleft()
                    exp.append(True)
                else:
                    exp.append(False)
            elif op == "Front":
                exp.append(d[0] if d else -1)
            elif op == "Rear":
                exp.append(d[-1] if d else -1)
            elif op == "isEmpty":
                exp.append(len(d) == 0)
            elif op == "isFull":
                exp.append(len(d) == k)
    return ops, args, exp


cases = []

# 1: example 1
cases.append((
    ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"],
    [[3], [1], [2], [3], [4], [], [], [], [4], []],
    [None, True, True, True, False, 3, True, True, True, 4],
))

# 2: capacity 1
cases.append((
    ["MyCircularQueue", "isEmpty", "isFull", "Front", "Rear", "deQueue", "enQueue", "enQueue",
     "Front", "Rear", "isFull", "isEmpty", "deQueue", "isEmpty", "enQueue", "Front"],
    [[1], [], [], [], [], [], [5], [6], [], [], [], [], [], [], [7], []],
    [None, True, False, -1, -1, False, True, False, 5, 5, True, False, True, True, True, 7],
))

# 3: operations on an empty queue
cases.append((
    ["MyCircularQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"],
    [[3], [], [], [], [], []],
    [None, False, -1, -1, True, False],
))

# 4: wrap-around
cases.append((
    ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "deQueue", "deQueue", "enQueue", "enQueue",
     "enQueue", "Front", "Rear", "isFull", "deQueue", "Front", "Rear", "enQueue", "Rear", "Front"],
    [[3], [1], [2], [3], [], [], [4], [5], [6], [], [], [], [], [], [], [0], [], []],
    [None, True, True, True, True, True, True, True, False, 3, 5, True, True, 4, 5, True, 0, 4],
))

# 5: value 0 is a valid element
cases.append((
    ["MyCircularQueue", "enQueue", "Front", "Rear", "isEmpty", "enQueue", "isFull", "deQueue",
     "Front", "deQueue", "Front", "isEmpty"],
    [[2], [0], [], [], [], [0], [], [], [], [], [], []],
    [None, True, 0, 0, False, True, True, True, 0, True, -1, True],
))

# 6: fill, drain, refill
cases.append((
    ["MyCircularQueue", "enQueue", "enQueue", "deQueue", "deQueue", "deQueue", "enQueue", "Front",
     "Rear", "enQueue", "Rear", "Front", "isFull"],
    [[2], [1], [2], [], [], [], [3], [], [], [4], [], [], []],
    [None, True, True, True, True, False, True, 3, 3, True, 4, 3, True],
))

# 7: duplicates
cases.append((
    ["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "deQueue", "Front", "enQueue",
     "Rear", "deQueue", "deQueue", "Front", "Rear", "deQueue", "isEmpty"],
    [[3], [7], [7], [7], [7], [], [], [8], [], [], [], [], [], [], []],
    [None, True, True, True, False, True, 7, True, 8, True, True, 8, 8, True, True],
))

# 8: large, capacity 1000 filled, then rotated many times
steps = [("enQueue", i) for i in range(1000)]
steps += [("enQueue", 1000), ("isFull", None), ("Front", None), ("Rear", None)]
for i in range(1000):
    steps += [("deQueue", None), ("enQueue", i % 1001)]
steps += [("Front", None), ("Rear", None), ("isFull", None), ("isEmpty", None)]
cases.append(model_run(1000, steps))

# 9: seeded random mix on a small ring
rng = random.Random(12345)
names = ["enQueue", "enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull"]
steps = []
for _ in range(2500):
    n = rng.choice(names)
    steps.append((n, rng.randint(0, 1000) if n == "enQueue" else None))
cases.append(model_run(7, steps))

# 10: seeded random, capacity 1, heavy churn
rng = random.Random(777)
steps = []
for _ in range(1000):
    n = rng.choice(names)
    steps.append((n, rng.randint(0, 1000) if n == "enQueue" else None))
cases.append(model_run(1, steps))

# 11: drain a full large queue to empty
steps = [("enQueue", i) for i in range(500)]
steps += [("deQueue", None) for _ in range(501)]
steps += [("isEmpty", None), ("Front", None), ("Rear", None), ("enQueue", 42), ("Front", None), ("Rear", None)]
cases.append(model_run(500, steps))


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


def same(got, exp):
    if isinstance(exp, bool):
        return isinstance(got, bool) and got == exp
    return got == exp and not isinstance(got, bool)


passed = 0
total = len(cases)
for idx, (ops, args, exp) in enumerate(cases, 1):
    try:
        obj = ns["MyCircularQueue"](*args[0])
        got = [None]
        bad = None
        for j in range(1, len(ops)):
            r = getattr(obj, ops[j])(*args[j])
            got.append(r)
            if not same(r, exp[j]):
                bad = j
                break
        if bad is None:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input=ops[{bad}]={ops[bad]}{args[bad]} (first {bad + 1} ops: "
                  f"{short(ops[:bad + 1])} {short(args[:bad + 1])}), "
                  f"expected={short(exp[bad])}, got={short(got[bad])}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(ops)} {short(args)}, expected={short(exp)}, "
              f"got=error {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)