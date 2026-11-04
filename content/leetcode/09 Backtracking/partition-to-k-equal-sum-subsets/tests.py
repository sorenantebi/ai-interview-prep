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
    # (nums, k, expected)
    ([4, 3, 2, 3, 5, 2, 1], 4, True),                      # example 1
    ([1, 2, 3, 4], 3, False),                              # example 2
    ([1], 1, True),                                        # single element
    ([5, 1, 2], 1, True),                                  # k = 1 always true
    ([1, 1, 1, 1], 4, True),                               # every element alone
    ([1, 1, 1, 1], 2, True),                               # duplicates
    ([3, 3, 3, 3], 3, False),                              # sum 12, target 4, not reachable
    ([1, 1, 1, 9], 2, False),                              # element larger than target
    ([2, 2, 2, 2, 3, 4, 5], 4, False),                     # divisible but impossible
    ([5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3], 4, True),       # 5+4+3 four times
    ([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4], 5, True),  # 16 elements, target 8
    (list(range(1, 17)), 8, True),                         # 16 elements, target 17
    (list(range(1, 17)), 3, False),                        # sum 136 not divisible by 3
]

passed = 0
total = len(cases)
for i, (nums, k, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().canPartitionKSubsets(list(nums), k)
        if got is expected or (isinstance(got, bool) and got == expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={(nums, k)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={(nums, k)}, expected={expected}, got=exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)