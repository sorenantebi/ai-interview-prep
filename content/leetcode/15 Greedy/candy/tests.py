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

N = 50000
mountain = list(range(N // 2)) + list(range(N // 2, 0, -1))

cases = [
    ([1, 0, 2], 5),
    ([1, 2, 2], 4),
    ([5], 1),
    ([1, 1, 1, 1], 4),
    ([1, 2, 3, 4, 5], 15),
    ([5, 4, 3, 2, 1], 15),
    ([1, 3, 2, 2, 1], 7),
    ([0, 0], 2),
    ([1, 2, 87, 87, 87, 2, 1], 13),
    ([2, 1], 3),
    ([1, 0, 2, 0, 2], 8),
    ([3, 2, 1, 2, 3], 11),
    (mountain, 625025001),
    ([7] * N, N),
    (list(range(N)), N * (N + 1) // 2),
]


def show(x):
    return f"<list of length {len(x)}>" if len(x) > 50 else repr(x)


passed = 0
for i, (ratings, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().candy(list(ratings))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={show(ratings)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={show(ratings)}, expected={expected}, got=error: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)