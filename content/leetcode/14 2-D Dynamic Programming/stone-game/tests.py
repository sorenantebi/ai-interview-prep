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


def make_large_pattern():
    piles = [(i * 37) % 500 + 1 for i in range(500)]
    if sum(piles) % 2 == 0:
        if piles[0] < 500:
            piles[0] += 1
        else:
            piles[0] -= 1
    return piles


# With an even number of piles and an odd total, Alice always wins.
cases = [
    ([5, 3, 4, 5], True),
    ([3, 7, 2, 3], True),
    ([1, 2], True),
    ([2, 1], True),
    ([1, 100], True),
    ([7, 7, 7, 6], True),
    ([1, 1, 1, 2], True),
    ([500, 1, 1, 499], True),
    ([3, 2, 10, 4], True),
    ([2, 2, 2, 3], True),
    ([1] * 499 + [2], True),
    (make_large_pattern(), True),
]

passed = 0
total = len(cases)
for idx, (piles, expected) in enumerate(cases, 1):
    shown = piles if len(piles) <= 10 else f"<{len(piles)} piles>"
    try:
        sol = ns["Solution"]()
        got = sol.stoneGame(list(piles))
        if got == expected and isinstance(got, bool):
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
