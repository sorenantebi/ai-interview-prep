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

# Large case: flower i blooms on [i, i + 99] for i in 1..50000
N = 50000
big_flowers = [[i, i + 99] for i in range(1, N + 1)]
big_people = list(range(1, N + 1)) + [50050, 60000, 10**9]


def big_expected():
    out = []
    for t in big_people:
        lo = max(1, t - 99)
        hi = min(N, t)
        out.append(max(0, hi - lo + 1))
    return out


cases = [
    ([[1, 6], [3, 7], [9, 12], [4, 13]], [2, 3, 7, 11], [1, 2, 2, 2]),
    ([[1, 10], [3, 3]], [3, 3, 2], [2, 2, 1]),
    ([[5, 5]], [4, 5, 6], [0, 1, 0]),
    ([[1, 1]], [1], [1]),
    ([[2, 4], [2, 4], [2, 4]], [1, 2, 3, 4, 5], [0, 3, 3, 3, 0]),
    ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1, 0]),
    ([[1, 10], [2, 9], [3, 8], [4, 7]], [5, 1, 10, 11], [4, 1, 1, 0]),
    ([[1, 10**9]], [1, 10**9, 500000000], [1, 1, 1]),
    ([[10, 20], [15, 25], [1, 5]], [25, 15, 5, 6, 10, 20, 1], [1, 2, 1, 0, 1, 2, 1]),
    ([[1, 3], [3, 5]], [3], [2]),
    (big_flowers, big_people, big_expected()),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 200 else s[:200] + "..."


passed = 0
total = len(cases)
for idx, (flowers, people, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.fullBloomFlowers([list(f) for f in flowers], list(people))
        got = list(got) if got is not None else got
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short((flowers, people))}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short((flowers, people))}, expected={short(expected)}, got=exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)