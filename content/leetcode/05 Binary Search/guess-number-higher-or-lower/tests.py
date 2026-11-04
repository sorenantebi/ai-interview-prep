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

MAX_CALLS = 40  # log2(2^31) is about 31, so a linear scan fails on large inputs


class TooManyCalls(Exception):
    pass


def make_guess(pick):
    calls = [0]

    def guess(num):
        calls[0] += 1
        if calls[0] > MAX_CALLS:
            raise TooManyCalls(f"guess called more than {MAX_CALLS} times")
        if num > pick:
            return -1
        if num < pick:
            return 1
        return 0

    return guess


BIG = 2 ** 31 - 1

# (n, pick, expected)
cases = [
    (10, 6, 6),
    (1, 1, 1),
    (2, 1, 1),
    (2, 2, 2),
    (3, 1, 1),
    (3, 3, 3),
    (10, 10, 10),
    (100, 1, 1),
    (100, 100, 100),
    (BIG, BIG, BIG),
    (BIG, 1, 1),
    (BIG, 123456789, 123456789),
    (BIG, BIG - 1, BIG - 1),
]

passed = 0
total = len(cases)
for i, (n, pick, expected) in enumerate(cases, 1):
    try:
        ns["guess"] = make_guess(pick)
        got = ns["Solution"]().guessNumber(n)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=n={n}, pick={pick}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=n={n}, pick={pick}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
