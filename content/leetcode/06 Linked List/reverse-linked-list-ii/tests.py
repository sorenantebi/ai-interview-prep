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
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head, limit=10000):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        if len(out) > limit:
            raise RuntimeError("list too long or contains a cycle")
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big = [i - 250 for i in range(500)]
big_full = big[::-1]
big_mid = big[:99] + big[99:400][::-1] + big[400:]

cases = [
    ([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5]),
    ([5], 1, 1, [5]),
    ([1, 2], 1, 2, [2, 1]),
    ([1, 2, 3], 1, 3, [3, 2, 1]),
    ([1, 2, 3, 4, 5], 1, 3, [3, 2, 1, 4, 5]),
    ([1, 2, 3, 4, 5], 3, 5, [1, 2, 5, 4, 3]),
    ([1, 2, 3, 4, 5], 3, 3, [1, 2, 3, 4, 5]),
    ([-1, -2, -3, -4], 2, 3, [-1, -3, -2, -4]),
    ([1, 1, 2, 2, 3, 3], 2, 5, [1, 3, 2, 2, 1, 3]),
    ([500, -500], 1, 1, [500, -500]),
    ([0, 1, 2, 3], 2, 2, [0, 1, 2, 3]),
    (big, 1, 500, big_full),
    (big, 100, 400, big_mid),
]

passed = 0
total = len(cases)
for i, (vals, left, right, expected) in enumerate(cases, 1):
    desc = f"head={vals if len(vals) <= 20 else '<%d nodes>' % len(vals)}, left={left}, right={right}"
    try:
        sol = ns["Solution"]()
        res = sol.reverseBetween(build_list(vals), left, right)
        got = list_to_array(res)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            exp_s = expected if len(expected) <= 20 else f"<{len(expected)} values>"
            got_s = got if len(got) <= 20 else f"<{len(got)} values>"
            print(f"FAIL case {i}: input={desc}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {i}: input={desc}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)