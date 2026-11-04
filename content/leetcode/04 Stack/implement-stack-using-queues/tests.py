import sys
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "deque": deque,
    "collections": __import__("collections"),
}
exec(open("attempt.py").read(), ns)


def replay(ops, args):
    obj = None
    out = []
    for op, a in zip(ops, args):
        if op == "MyStack":
            obj = ns["MyStack"](*a)
            out.append(None)
        else:
            res = getattr(obj, op)(*a)
            out.append(res if op in ("pop", "top", "empty") else None)
    return out


def make(seq):
    """seq: list of (op, arg-or-None); prepends constructor."""
    ops = ["MyStack"]
    args = [[]]
    for op, a in seq:
        ops.append(op)
        args.append([] if a is None else [a])
    return ops, args


N = None
cases = []

# 1: example
cases.append((
    ["MyStack", "push", "push", "top", "pop", "empty"],
    [[], [1], [2], [], [], []],
    [N, N, N, 2, 2, False],
))

# 2: empty new stack
o, a = make([("empty", None)])
cases.append((o, a, [N, True]))

# 3: single element
o, a = make([("push", 5), ("top", None), ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, 5, 5, True]))

# 4: full LIFO drain
o, a = make([("push", 1), ("push", 2), ("push", 3), ("pop", None), ("pop", None),
             ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, N, N, 3, 2, 1, True]))

# 5: duplicates
o, a = make([("push", 4), ("push", 4), ("push", 4), ("pop", None), ("top", None),
             ("pop", None), ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, N, N, 4, 4, 4, 4, True]))

# 6: interleaved
o, a = make([("push", 1), ("push", 2), ("pop", None), ("push", 3), ("top", None),
             ("pop", None), ("top", None), ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, N, 2, N, 3, 3, 1, 1, True]))

# 7: top does not remove
o, a = make([("push", 7), ("top", None), ("top", None), ("top", None), ("empty", None)])
cases.append((o, a, [N, N, 7, 7, 7, False]))

# 8: alternating push/pop
o, a = make([("push", 1), ("pop", None), ("push", 2), ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, 1, N, 2, True]))

# 9: build up, partial pop, push again
o, a = make([("push", 1), ("push", 2), ("push", 3), ("push", 4), ("push", 5),
             ("top", None), ("pop", None), ("pop", None), ("push", 9),
             ("top", None), ("pop", None), ("top", None), ("empty", None)])
cases.append((o, a, [N, N, N, N, N, N, 5, 5, 4, N, 9, 9, 3, False]))

# 10: becomes empty then reused
o, a = make([("push", 2), ("push", 3), ("pop", None), ("pop", None), ("empty", None),
             ("push", 1), ("empty", None), ("top", None)])
cases.append((o, a, [N, N, N, 3, 2, True, N, False, 1]))

# 11: boundary values 1 and 9
o, a = make([("push", 9), ("push", 1), ("top", None), ("pop", None), ("top", None),
             ("pop", None), ("empty", None)])
cases.append((o, a, [N, N, N, 1, 1, 9, 9, True]))

# 12: larger input (expected computed by a plain-list model: reverse of pushes)
pushes = [(i % 9) + 1 for i in range(1000)]
o, a = make([("push", v) for v in pushes] + [("pop", None)] * 1000 + [("empty", None)])
cases.append((o, a, [N] * 1001 + list(reversed(pushes)) + [True]))

passed = 0
for i, (ops, args, expected) in enumerate(cases, 1):
    try:
        got = replay(ops, args)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            s = f"ops={ops}, args={args}"
            e, g = expected, got
            if len(s) > 200:
                s = f"ops[{len(ops)}]..."
                e, g = str(expected)[:100] + "...", str(got)[:100] + "..."
            print(f"FAIL case {i}: input={s}, expected={e}, got={g}")
    except Exception as ex:
        print(f"FAIL case {i}: input=ops[{len(ops)}], error={type(ex).__name__}: {ex}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
