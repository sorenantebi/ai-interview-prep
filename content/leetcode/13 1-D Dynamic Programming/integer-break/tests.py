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
    (2, 1),
    (3, 2),
    (4, 4),
    (5, 6),
    (6, 9),
    (7, 12),
    (10, 36),
    (11, 54),
    (15, 243),
    (20, 1458),
    (25, 8748),
    (30, 59049),
    (58, 1549681956),
]

passed = 0
total = len(cases)
for i, (n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().integerBreak(n)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={n}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={n}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)