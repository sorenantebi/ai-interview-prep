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

cases = [
    ([1, 1, 2, 2, 2], True),
    ([3, 3, 3, 3, 4], False),
    ([1], False),
    ([1, 1, 1, 1], True),
    ([5, 5, 5, 5], True),
    ([1, 2, 3, 4], False),          # sum 10, not divisible by 4
    ([5, 1, 1, 1], False),          # longest exceeds side (2)
    ([2] * 8, True),                # side 4, two per side
    ([10 ** 8] * 4, True),
    ([10 ** 8] * 8, True),          # large values, side 2e8
    ([3] * 8 + [4], False),         # side 7, 3s cannot make 7
    ([1] * 14 + [2], True),         # side 4
    ([3] * 12, True),               # side 9, three per side
    ([4], False),
]

passed = 0
total = len(cases)
for n, (inp, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.makesquare(list(inp))
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={inp}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)