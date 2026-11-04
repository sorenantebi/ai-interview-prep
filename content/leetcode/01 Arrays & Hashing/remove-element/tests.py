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

big = [i % 51 for i in range(100)]

# (nums, val, expected_k, expected_sorted_remaining)
CASES = [
    ([3, 2, 2, 3], 3, 2, [2, 2]),
    ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5, [0, 0, 1, 3, 4]),
    ([], 0, 0, []),
    ([1], 1, 0, []),
    ([1], 2, 1, [1]),
    ([4, 4, 4, 4], 4, 0, []),
    ([1, 2, 3], 5, 3, [1, 2, 3]),
    ([0, 0, 1], 0, 1, [1]),
    ([50, 0, 50, 25], 50, 2, [0, 25]),
    (big, 0, 98, sorted(x for x in big if x != 0)),
    ([2, 2, 2, 3, 2], 2, 1, [3]),
    ([3, 3, 2, 3, 3], 3, 1, [2]),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (nums, val, exp_k, exp_rest) in enumerate(CASES, 1):
        arr = list(nums)
        try:
            sol = ns["Solution"]()
            k = sol.removeElement(arr, val)
            got_rest = sorted(arr[:k]) if isinstance(k, int) and 0 <= k <= len(arr) else None
            if k == exp_k and got_rest == exp_rest:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input=(nums={nums}, val={val}), "
                      f"expected=(k={exp_k}, sorted_first_k={exp_rest}), "
                      f"got=(k={k}, sorted_first_k={got_rest})")
        except Exception as e:
            print(f"FAIL case {n}: input=(nums={nums}, val={val}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()