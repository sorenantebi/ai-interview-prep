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

BIG = list(range(0, 20000, 2))  # 10000 elements, index i holds 2*i

# (nums, target, expected)
CASES = [
    ([1, 3, 5, 6], 5, 2),
    ([1, 3, 5, 6], 2, 1),
    ([1, 3, 5, 6], 7, 4),
    ([1], 1, 0),
    ([1], 0, 0),
    ([1], 2, 1),
    ([1, 3], 3, 1),
    ([1, 3], 2, 1),
    ([-10, -5, 0, 5, 10], -7, 1),
    ([-10, -5, 0, 5, 10], -10, 0),
    ([-10, -5, 0, 5, 10], 11, 5),
    ([-10, -5, 0, 5, 10], 10, 4),
    (BIG, 9999, 5000),    # between 9998 (idx 4999) and 10000 (idx 5000)
    (BIG, 19999, 10000),  # greater than last element 19998 -> append
    (BIG, 19998, 9999),   # last element present at idx 9999
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


def main():
    passed = 0
    total = len(CASES)
    for i, (nums, target, expected) in enumerate(CASES, 1):
        inp = (list(nums), target)
        try:
            got = ns["Solution"]().searchInsert(list(nums), target)
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input={short(inp)}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input={short(inp)}, expected={expected}, got=error: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
