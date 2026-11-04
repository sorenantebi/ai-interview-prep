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
    (4, 2),
    (8, 2),
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 1),
    (9, 3),
    (15, 3),
    (16, 4),
    (99999999, 9999),
    (2147395599, 46339),
    (2147395600, 46340),
    (2147483647, 46340),
]

passed = 0
total = len(cases)
for i, (x, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().mySqrt(x)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={x}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={x}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)