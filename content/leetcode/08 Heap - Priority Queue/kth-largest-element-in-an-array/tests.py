import sys
import random
import heapq
from heapq import heapify, heappop, heappush, heapreplace, nlargest, nsmallest
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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = [root]
    i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
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
    "random": random,
    "heapq": heapq,
    "heapify": heapify,
    "heappop": heappop,
    "heappush": heappush,
    "heapreplace": heapreplace,
    "nlargest": nlargest,
    "nsmallest": nsmallest,
}
exec(open("attempt.py").read(), ns)


def expected_for(nums, k):
    return sorted(nums, reverse=True)[k - 1]


rng = random.Random(12345)
large_nums = [rng.randint(-10000, 10000) for _ in range(100000)]
sorted_asc = list(range(-5000, 5000))
sorted_desc = sorted_asc[::-1]

cases = [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
    ([1], 1, 1),
    ([-1], 1, -1),
    ([7, 7, 7, 7], 3, 7),
    ([-5, -1, -3, -2, -4], 2, -2),
    ([2, 1], 1, 2),
    ([2, 1], 2, 1),
    ([5, 5, 4, 4, 3, 3], 3, 4),
    ([-10000, 10000, 0], 2, 0),
    (sorted_asc, 10, None),
    (sorted_desc, 5000, None),
    (large_nums, 50000, None),
    (large_nums, 1, None),
    (large_nums, 100000, None),
]


def run():
    passed = 0
    total = len(cases)
    for i, (nums, k, exp) in enumerate(cases, 1):
        if exp is None:
            exp = expected_for(nums, k)
        shown = nums if len(nums) <= 20 else f"<list len={len(nums)}>"
        try:
            arg = list(nums)  # solution may mutate input
            got = ns["Solution"]().findKthLargest(arg, k)
            if got == exp:
                print(f"PASS case {i}")
                passed += 1
            else:
                print(f"FAIL case {i}: input=(nums={shown}, k={k}), expected={exp}, got={got}")
        except Exception as e:
            print(f"FAIL case {i}: input=(nums={shown}, k={k}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()