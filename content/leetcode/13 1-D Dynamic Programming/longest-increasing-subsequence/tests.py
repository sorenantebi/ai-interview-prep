import sys
import random
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
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def brute(nums):
    # O(n^2) reference DP for random cases
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


random.seed(12345)
rand_small = [random.randint(-10, 10) for _ in range(30)]
rand_large = [random.randint(-10000, 10000) for _ in range(2500)]

cases = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4),
    ([0, 1, 0, 3, 2, 3], 4),
    ([7, 7, 7, 7, 7, 7, 7], 1),
    ([5], 1),
    ([1, 2], 2),
    ([2, 1], 1),
    ([1, 2, 3, 4, 5, 6], 6),
    ([6, 5, 4, 3, 2, 1], 1),
    ([-3, -2, -1, 0, 1], 5),
    ([4, 10, 4, 3, 8, 9], 3),
    (rand_small, brute(rand_small)),
    (list(range(-1250, 1250)), 2500),
    (list(range(2500, 0, -1)), 1),
    (rand_large, brute(rand_large)),
]

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 40 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().lengthOfLIS(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=Exception({type(e).__name__}: {e})")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)