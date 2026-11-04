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

# (n, x, expected)
CASES = [
    (3, 4, 6),
    (2, 7, 15),
    (1, 1, 1),
    (1, 10**8, 10**8),
    (2, 1, 3),
    (4, 1, 7),
    (5, 2, 10),
    (3, 5, 13),
    (6, 8, 13),
    (7, 6, 30),
    (10**8, 1, 199999999),
    (10**8, 2**26 - 1, 6710886399999999),
]


def main():
    passed = 0
    total = len(CASES)
    for i, (n, x, expected) in enumerate(CASES, 1):
        try:
            got = ns["Solution"]().minEnd(n, x)
            if got == expected:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input=(n={n}, x={x}), expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input=(n={n}, x={x}), expected={expected}, got=error: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()
