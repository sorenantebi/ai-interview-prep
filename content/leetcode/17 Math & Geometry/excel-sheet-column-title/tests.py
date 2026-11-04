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
    (1, "A"),
    (28, "AB"),
    (701, "ZY"),
    (26, "Z"),
    (27, "AA"),
    (52, "AZ"),
    (53, "BA"),
    (676, "YZ"),
    (702, "ZZ"),
    (703, "AAA"),
    (18278, "ZZZ"),
    (2147483647, "FXSHRXW"),
]

passed = 0
total = len(cases)
for i, (n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().convertToTitle(n)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={n}, expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={n}, expected={expected!r}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
