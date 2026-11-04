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
    (7, [2, 3, 1, 2, 4, 3], 2),
    (4, [1, 4, 4], 1),
    (11, [1] * 8, 0),
    (5, [5], 1),
    (6, [5], 0),
    (15, [1, 2, 3, 4, 5], 5),
    (11, [1, 2, 3, 4, 5], 3),
    (9, [1, 2, 3, 4, 5], 2),
    (213, [12, 28, 83, 4, 25, 26, 25, 2, 25, 25, 25, 12], 8),
    (3, [1, 1], 0),
    (10 ** 9, [10000] * 100000, 100000),
    (50000, [1] * 100000, 50000),
    (10 ** 9, [1] * 100000, 0),
]

passed = 0
total = len(cases)
for i, (target, nums, expected) in enumerate(cases, 1):
    desc = f"target={target}, nums={nums if len(nums) <= 20 else f'<list of {len(nums)}>'}"
    try:
        got = ns["Solution"]().minSubArrayLen(target, list(nums))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={desc}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)