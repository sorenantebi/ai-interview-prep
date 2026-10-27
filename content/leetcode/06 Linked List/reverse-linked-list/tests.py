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


def list_to_array(head, limit=100000):
    out = []
    seen = 0
    while head is not None:
        out.append(head.val)
        head = head.next
        seen += 1
        if seen > limit:
            raise RuntimeError("cycle or overlong list detected in result")
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def run(vals):
    sol = ns["Solution"]()
    return list_to_array(sol.reverseList(build_list(vals)))


cases = [
    [1, 2, 3, 4, 5],
    [1, 2],
    [],
    [7],
    [-1, -2, -3],
    [0, 0, 0],
    [1, 1, 2, 2, 3],
    [-5000, 5000],
    [5000, -5000, 0, 1],
    list(range(5000)),
    [i % 7 - 3 for i in range(5000)],
    [1, 2, 3],
]

passed = 0
total = len(cases)
for i, vals in enumerate(cases, 1):
    expected = list(reversed(vals))
    shown = vals if len(vals) <= 20 else f"<{len(vals)} elements>"
    try:
        got = run(vals)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            exp_s = expected if len(expected) <= 20 else f"<{len(expected)} elements>"
            got_s = got if len(got) <= 20 else f"<{len(got)} elements>"
            print(f"FAIL case {i}: input={shown}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)