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

B = 10**9

cases = [
    ([1, 0, -1, 0, -2, 2], 0, [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
    ([2, 2, 2, 2, 2], 8, [[2, 2, 2, 2]]),
    ([0, 0, 0, 0], 0, [[0, 0, 0, 0]]),
    ([1], 1, []),
    ([1, 2, 3], 6, []),
    ([-B, -B, B, B], 0, [[-B, -B, B, B]]),
    ([B, B, B, B], B, []),
    ([-3, -2, -1, 0, 0, 1, 2, 3], 0,
     [[-3, -2, 2, 3], [-3, -1, 1, 3], [-3, 0, 0, 3], [-3, 0, 1, 2],
      [-2, -1, 0, 3], [-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
    ([-1, 0, 1, 2, -1, -4], -1, [[-4, 0, 1, 2], [-1, -1, 0, 1]]),
    ([1, 2, 3, 4, 5], 100, []),
    ([0] * 7, 0, [[0, 0, 0, 0]]),
    ([1, 1, 1, 1, 2, 2, 2, 2], 6, [[1, 1, 2, 2]]),
    (list(range(200)), 10, [[0, 1, 2, 7], [0, 1, 3, 6], [0, 1, 4, 5], [0, 2, 3, 5], [1, 2, 3, 4]]),
    ([0] * 200, 0, [[0, 0, 0, 0]]),
]


def canon(res):
    return sorted(sorted(q) for q in res)


passed = 0
total = len(cases)
for idx, (nums, target, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 12 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().fourSum(list(nums), target)
        if canon(got) == canon(expected):
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=({shown}, {target}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({shown}, {target}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)