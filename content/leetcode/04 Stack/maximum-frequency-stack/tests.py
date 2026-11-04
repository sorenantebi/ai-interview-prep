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
FreqStack = ns["FreqStack"]


def P(v):
    return ("push", v)


def Q(expected):
    return ("pop", expected)


def build_ops(pushes, pops):
    return [P(v) for v in pushes] + [Q(e) for e in pops]


B = 10 ** 9

cases = []

# 1: example
cases.append(build_ops([5, 7, 5, 7, 4, 5], [5, 7, 5, 4]))
# 2: single element
cases.append([P(3), Q(3)])
# 3: all same
cases.append(build_ops([1, 1, 1], [1, 1, 1]))
# 4: all distinct -> LIFO
cases.append(build_ops([1, 2, 3], [3, 2, 1]))
# 5: boundary values 0 and 1e9
cases.append(build_ops([0, B, 0, B], [B, 0, B, 0]))
# 6: interleaved push/pop
cases.append([P(1), P(2), Q(2), P(1), Q(1), Q(1), P(3), Q(3)])
# 7: ties at several levels
cases.append(build_ops([1, 1, 2, 2, 3], [2, 1, 3, 2, 1]))
# 8: three-way frequencies
cases.append(build_ops([1, 2, 1, 3, 1, 2, 3], [1, 3, 2, 1, 3, 2, 1]))
# 9: frequency 3 then ties
cases.append(build_ops([4, 4, 5, 5, 4], [4, 5, 4, 5, 4]))
# 10: large, all same value
cases.append(build_ops([7] * 10000, [7] * 10000))
# 11: large, 100 values each pushed 100 times; layers pop 99..0
cases.append(build_ops([i % 100 for i in range(10000)], list(range(99, -1, -1)) * 100))
# 12: large, all distinct
cases.append(build_ops(list(range(10000)), list(range(9999, -1, -1))))


def describe(ops):
    s = str(ops)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
total = len(cases)
for i, ops in enumerate(cases, 1):
    expected = [e for kind, e in ops if kind == "pop"]
    got = []
    try:
        fs = FreqStack()
        for kind, arg in ops:
            if kind == "push":
                fs.push(arg)
            else:
                got.append(fs.pop())
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            es, gs = str(expected), str(got)
            if len(es) > 200:
                es = es[:200] + "..."
            if len(gs) > 200:
                gs = gs[:200] + "..."
            print(f"FAIL case {i}: input={describe(ops)}, expected={es}, got={gs}")
    except Exception as e:
        print(f"FAIL case {i}: input={describe(ops)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)