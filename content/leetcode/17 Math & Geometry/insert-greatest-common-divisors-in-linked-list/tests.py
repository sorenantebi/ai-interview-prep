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


def list_to_array(head, limit=100000):
    out = []
    while head is not None and len(out) <= limit:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

# Large case: alternating 1000, 750 -> every gcd is 250
_large_in = [1000 if i % 2 == 0 else 750 for i in range(5000)]
_large_out = []
for _i, _v in enumerate(_large_in):
    _large_out.append(_v)
    if _i < len(_large_in) - 1:
        _large_out.append(250)

cases = [
    ([18, 6, 10, 3], [18, 6, 6, 2, 10, 1, 3]),
    ([7], [7]),
    ([4, 4], [4, 4, 4]),
    ([2, 3], [2, 1, 3]),
    ([1, 1, 1], [1, 1, 1, 1, 1]),
    ([12, 18], [12, 6, 18]),
    ([1000, 1000, 1000], [1000, 1000, 1000, 1000, 1000]),
    ([6, 12, 24, 48], [6, 6, 12, 12, 24, 24, 48]),
    ([9, 28, 35, 14], [9, 1, 28, 7, 35, 7, 14]),
    ([100, 75, 50, 25], [100, 25, 75, 25, 50, 25, 25]),
    ([999, 1000], [999, 1, 1000]),
    ([17, 34, 51, 68], [17, 17, 34, 17, 51, 17, 68]),
    (_large_in, _large_out),
]

passed = 0
total = len(cases)
for n, (inp, expected) in enumerate(cases, 1):
    shown = inp if len(inp) <= 20 else f"<list of {len(inp)} nodes>"
    try:
        sol = ns["Solution"]()
        result = sol.insertGreatestCommonDivisors(build_list(inp))
        got = list_to_array(result)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            exp_shown = expected if len(expected) <= 40 else f"<{len(expected)} values>"
            got_shown = got if len(got) <= 40 else f"<{len(got)} values>"
            print(f"FAIL case {n}: input={shown}, expected={exp_shown}, got={got_shown}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)