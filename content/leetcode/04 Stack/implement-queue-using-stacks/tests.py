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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def replay(ops, args):
    obj = None
    out = []
    for op, a in zip(ops, args):
        if op == "MyQueue":
            obj = ns["MyQueue"](*a)
            out.append(None)
        else:
            out.append(getattr(obj, op)(*a))
    return out


N = None
cases = []

# 1: example
cases.append((
    ["MyQueue", "push", "push", "peek", "pop", "empty"],
    [[], [1], [2], [], [], []],
    [N, N, N, 1, 1, False],
))
# 2: new queue is empty
cases.append((["MyQueue", "empty"], [[], []], [N, True]))
# 3: single element
cases.append((
    ["MyQueue", "push", "empty", "pop", "empty"],
    [[], [5], [], [], []],
    [N, N, False, 5, True],
))
# 4: peek does not remove
cases.append((
    ["MyQueue", "push", "peek", "peek", "pop", "empty"],
    [[], [3], [], [], [], []],
    [N, N, 3, 3, 3, True],
))
# 5: interleaved push/pop
cases.append((
    ["MyQueue", "push", "push", "pop", "push", "pop", "push", "peek", "pop", "pop", "empty"],
    [[], [1], [2], [], [3], [], [4], [], [], [], []],
    [N, N, N, 1, N, 2, N, 3, 3, 4, True],
))
# 6: duplicates
cases.append((
    ["MyQueue", "push", "push", "push", "pop", "pop", "peek", "pop", "empty"],
    [[], [7], [7], [7], [], [], [], [], []],
    [N, N, N, N, 7, 7, 7, 7, True],
))
# 7: fill 1..9, drain in order
cases.append((
    ["MyQueue"] + ["push"] * 9 + ["pop"] * 9 + ["empty"],
    [[]] + [[i] for i in range(1, 10)] + [[]] * 9 + [[]],
    [N] + [N] * 9 + list(range(1, 10)) + [True],
))
# 8: reuse after becoming empty
cases.append((
    ["MyQueue", "push", "pop", "empty", "push", "peek", "empty"],
    [[], [1], [], [], [2], [], []],
    [N, N, 1, True, N, 2, False],
))
# 9: peek after transfer, then more pushes
cases.append((
    ["MyQueue", "push", "push", "peek", "push", "pop", "pop", "peek", "empty"],
    [[], [1], [2], [], [3], [], [], [], []],
    [N, N, N, 1, N, 1, 2, 3, False],
))
# 10: boundary values
cases.append((
    ["MyQueue", "push", "push", "pop", "empty", "pop", "empty"],
    [[], [9], [1], [], [], [], []],
    [N, N, N, 9, False, 1, True],
))
# 11: large input (amortized O(1) needed)
big = 20000
seq = [(i % 9) + 1 for i in range(big)]
cases.append((
    ["MyQueue"] + ["push"] * big + ["pop"] * big + ["empty"],
    [[]] + [[v] for v in seq] + [[]] * big + [[]],
    [N] + [N] * big + seq + [True],
))
# 12: large interleaved, push 2 / pop 1 pattern with peeks
ops12 = ["MyQueue"]
args12 = [[]]
exp12 = [N]
ref = []
head = 0
for i in range(5000):
    for v in ((i % 9) + 1, ((i * 2) % 9) + 1):
        ops12.append("push"); args12.append([v]); exp12.append(N)
        ref.append(v)
    ops12.append("peek"); args12.append([]); exp12.append(ref[head])
    ops12.append("pop"); args12.append([]); exp12.append(ref[head])
    head += 1
ops12.append("empty"); args12.append([]); exp12.append(head == len(ref))
cases.append((ops12, args12, exp12))


def short(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
for i, (ops, args, expected) in enumerate(cases, 1):
    try:
        got = replay(ops, args)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={short((ops, args))}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short((ops, args))}, error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)