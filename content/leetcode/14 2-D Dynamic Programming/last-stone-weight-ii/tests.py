import sys
import math
import collections
import functools
import heapq
import itertools
import bisect
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    # names the reference solution uses without importing
    "ceil": math.ceil,
    "floor": math.floor,
    "math": math,
    "collections": collections,
    "functools": functools,
    "heapq": heapq,
    "itertools": itertools,
    "bisect": bisect,
    "cache": functools.cache,
    "lru_cache": functools.lru_cache,
    "defaultdict": collections.defaultdict,
    "Counter": collections.Counter,
    "deque": collections.deque,
}
exec(open("attempt.py").read(), ns)

cases = [
    ([2, 7, 4, 1, 8, 1], 1),
    ([31, 26, 33, 21, 40], 5),
    ([1], 1),
    ([1, 1], 0),
    ([100], 100),
    ([1, 2], 1),
    ([3, 3, 3], 3),
    ([100, 1], 99),
    ([10, 10, 10, 10, 10], 10),
    ([1, 2, 3, 4, 5], 1),
    ([99, 1, 1, 1], 96),
    ([100] * 30, 0),
    ([100] * 29, 100),
    ([1] * 29, 1),
]

passed = 0
total = len(cases)
for i, (stones, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().lastStoneWeightII(list(stones))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={stones}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={stones}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
