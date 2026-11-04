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


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


big = []
for v in range(-100, 101):
    big.extend([v] * 149)
big.extend([100] * 51)

cases = [
    ([1, 1, 2], [1, 2]),
    ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [0, 1, 2, 3, 4]),
    ([5], [5]),
    ([7, 7, 7, 7], [7]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([-3, -3, -2, -1, -1, 0, 0], [-3, -2, -1, 0]),
    ([-100, 100], [-100, 100]),
    ([1, 1], [1]),
    ([-100] * 5 + [0] * 3 + [100] * 4, [-100, 0, 100]),
    ([1, 2, 2], [1, 2]),
    ([1, 1, 1, 2, 3, 3], [1, 2, 3]),
    (big, list(range(-100, 101))),
    ([0] * 30000, [0]),
]

passed = 0
total = len(cases)

for i, (inp, exp) in enumerate(cases, 1):
    nums = list(inp)
    try:
        k = ns["Solution"]().removeDuplicates(nums)
        if k == len(exp) and nums[:k] == exp:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(inp)}, expected={len(exp)}, {short(exp)}, "
                  f"got={k}, {short(nums[:k] if isinstance(k, int) and k >= 0 else nums)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)