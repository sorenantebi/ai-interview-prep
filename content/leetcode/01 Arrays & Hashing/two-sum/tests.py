import sys
import time
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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def serialize_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def serialize_tree(root):
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "..."


large_nums = [2 * i for i in range(9998)] + [10**9, 1]

cases = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([3, 3], 6, [0, 1]),
    ([1, 2], 3, [0, 1]),
    ([-3, 4, 3, 90], 0, [0, 2]),
    ([-1, -2, -3, -4, -5], -8, [2, 4]),
    ([0, 4, 3, 0], 0, [0, 3]),
    ([10**9, -10**9, 5], 0, [0, 1]),
    ([1, 2, 3, 4, 50, 60], 110, [4, 5]),
    ([5, 5, 1, 10], 11, [2, 3]),
    ([4, 1, 7, 3], 5, [0, 1]),
    (large_nums, 10**9 + 1, [9998, 9999]),
]

TIME_LIMIT = 2.0
passed = 0
for n, (nums, target, expected) in enumerate(cases, 1):
    try:
        start = time.perf_counter()
        got = Solution().twoSum(list(nums), target)
        elapsed = time.perf_counter() - start
        got_cmp = sorted(list(got)) if got is not None else got
        if got_cmp != sorted(expected):
            print(f"FAIL case {n}: input=nums={short(nums)}, target={target}, expected={expected}, got={got}")
        elif elapsed > TIME_LIMIT:
            print(f"FAIL case {n}: input=nums={short(nums)}, target={target}, expected={expected}, got={got} (too slow: {elapsed:.2f}s)")
        else:
            print(f"PASS case {n}")
            passed += 1
    except Exception as e:
        print(f"FAIL case {n}: input=nums={short(nums)}, target={target}, expected={expected}, got={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)