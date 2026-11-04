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
    ([1, 2, 3, 7], "Bob"),
    ([1, 2, 3, -9], "Alice"),
    ([1, 2, 3, 6], "Tie"),
    ([1, 2, 3, -1, -2, -3, 7], "Alice"),
    ([5], "Alice"),
    ([-5], "Bob"),
    ([0], "Tie"),
    ([1, 2], "Alice"),
    ([-1, -2, -3], "Tie"),
    ([-1, -1, -1, -1], "Tie"),
    ([1] * 49998, "Tie"),
    ([1] * 50000, "Alice"),
]

passed = 0
total = len(cases)
for i, (stones, expected) in enumerate(cases, 1):
    shown = stones if len(stones) <= 20 else f"[{stones[0]}]*{len(stones)}"
    try:
        sol = ns["Solution"]()
        got = sol.stoneGameIII(list(stones))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={shown}, expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown}, expected={expected!r}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
