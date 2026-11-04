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
    ([2, 3, 6], True),
    ([3, 9, 5], False),
    ([4, 3, 12, 8], True),
    ([1], True),
    ([7], True),
    ([1, 1], False),
    ([1, 2], False),
    ([2, 2], True),
    ([6, 10, 15], True),
    ([2, 3, 5, 7], False),
    ([99991, 99991], True),
    ([99991, 2], False),
    ([6] * 50000 + [35] * 50000, False),
    ([6] * 50000 + [35] * 49999 + [10], True),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for i, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().canTraverseAllPairs(list(nums))
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)