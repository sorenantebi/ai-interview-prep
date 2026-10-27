import sys
import random
import collections
import heapq
import math
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


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = collections.deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = collections.deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "collections": collections,
    "heapq": heapq,
    "math": math,
    "itertools": itertools,
    "bisect": bisect,
}
with open("attempt.py") as f:
    exec(f.read(), ns)


def reference(nums, k):
    out = []
    dq = collections.deque()
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


rng = random.Random(12345)

big_random = [rng.randint(-10000, 10000) for _ in range(100000)]
big_increasing = list(range(-10000, 10001)) * 5
big_increasing.sort()
big_decreasing = sorted(big_increasing, reverse=True)

cases = [
    ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
    ([1], 1, [1]),
    ([1, -1], 1, [1, -1]),
    ([9, 11], 2, [11]),
    ([4, 3, 2, 1], 2, [4, 3, 2]),
    ([1, 2, 3, 4], 2, [2, 3, 4]),
    ([5, 5, 5, 5, 5], 3, [5, 5, 5]),
    ([-5, -3, -8, -1, -9, -2], 2, [-3, -3, -1, -1, -2]),
    ([7, 2, 4], 3, [7]),
    ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
    ([10, 9, 9, 8, 10, 7, 7], 3, [10, 9, 10, 10, 10]),
    (big_random, 50000, None),
    (big_random, 3, None),
    (big_increasing, 1000, None),
    (big_decreasing, 1000, None),
]

passed = 0
total = len(cases)
for idx, (nums, k, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(nums, k)
    label_nums = nums if len(nums) <= 30 else f"<list len={len(nums)}>"
    try:
        sol = ns["Solution"]()
        got = sol.maxSlidingWindow(list(nums), k)
        got = list(got) if got is not None else got
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            exp_s = expected if len(expected) <= 30 else f"<list len={len(expected)}>"
            got_s = got if got is None or len(got) <= 30 else f"<list len={len(got)}>"
            print(f"FAIL case {idx}: input=(nums={label_nums}, k={k}), expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {idx}: input=(nums={label_nums}, k={k}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
