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


def reference_large(piles):
    # independent bottom-up DP, used only for the large generated case
    n = len(piles)
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + piles[i]
    dp = [[0] * (n + 2) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for M in range(1, n + 1):
            if i + 2 * M >= n:
                dp[i][M] = suf[i]
            else:
                dp[i][M] = max(suf[i] - dp[i + X][max(M, X)] for X in range(1, 2 * M + 1))
    return dp[0][1]


large = [((i * 37) % 100 + 1) * 100 for i in range(100)]

cases = [
    ([2, 7, 9, 4, 4], 10),
    ([1, 2, 3, 4, 5, 100], 104),
    ([1], 1),
    ([5], 5),
    ([2, 3], 5),
    ([3, 1, 2], 4),
    ([1, 1, 1, 1], 2),
    ([1, 100, 1], 101),
    ([1, 2, 3, 4], 5),
    ([10000] * 2, 20000),
    (large, reference_large(large)),
]

passed = 0
total = len(cases)
for idx, (piles, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().stoneGameII(list(piles))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = piles if len(piles) <= 20 else f"<{len(piles)} piles>"
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        shown = piles if len(piles) <= 20 else f"<{len(piles)} piles>"
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)