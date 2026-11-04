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

# (n, expected)
CASES = [
    (4, 2),    # example 1
    (1, 1),    # example 2
    (2, 0),
    (3, 0),
    (5, 10),
    (6, 4),
    (7, 40),
    (8, 92),
    (9, 352),  # largest allowed input
]


def main():
    passed = 0
    total = 0
    sol = None
    try:
        sol = ns["Solution"]()
    except Exception as e:
        sol = None
        init_err = e

    for n, expected in CASES:
        total += 1
        try:
            if sol is None:
                raise RuntimeError(f"cannot create Solution: {init_err}")
            got = sol.totalNQueens(n)
            if got == expected:
                print(f"PASS case {total}")
                passed += 1
            else:
                print(f"FAIL case {total}: input=n={n}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {total}: input=n={n}, expected={expected}, got=error: {e}")

    # repeated calls on the same instance must not leak state
    total += 1
    try:
        if sol is None:
            raise RuntimeError(f"cannot create Solution: {init_err}")
        got = [sol.totalNQueens(6), sol.totalNQueens(4), sol.totalNQueens(6)]
        expected = [4, 2, 4]
        if got == expected:
            print(f"PASS case {total}")
            passed += 1
        else:
            print(f"FAIL case {total}: input=n=[6, 4, 6] on one instance, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {total}: input=n=[6, 4, 6] on one instance, expected=[4, 2, 4], got=error: {e}")

    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()