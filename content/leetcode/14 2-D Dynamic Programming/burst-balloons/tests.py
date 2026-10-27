import sys
import random
from itertools import permutations
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
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def ref_dp(nums):
    vals = [1] + list(nums) + [1]
    n = len(vals)
    dp = [[0] * n for _ in range(n)]
    for gap in range(2, n):
        for l in range(n - gap):
            r = l + gap
            best = 0
            for k in range(l + 1, r):
                c = dp[l][k] + vals[l] * vals[k] * vals[r] + dp[k][r]
                if c > best:
                    best = c
            dp[l][r] = best
    return dp[0][n - 1]


def ref_brute(nums):
    best = 0
    for order in permutations(range(len(nums))):
        alive = list(range(len(nums)))
        total = 0
        for idx in order:
            pos = alive.index(idx)
            left = nums[alive[pos - 1]] if pos > 0 else 1
            right = nums[alive[pos + 1]] if pos + 1 < len(alive) else 1
            total += left * nums[idx] * right
            alive.pop(pos)
        best = max(best, total)
    return best


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

rng = random.Random(12345)
rand_small = [rng.randint(0, 100) for _ in range(7)]
rand_mid = [rng.randint(0, 100) for _ in range(60)]
rand_large = [rng.randint(0, 100) for _ in range(300)]

cases = [
    ([3, 1, 5, 8], 167),
    ([1, 5], 10),
    ([5], 5),
    ([0], 0),
    ([0, 0, 0], 0),
    ([2, 2], 6),
    ([1] * 10, 10),
    ([1, 2, 3, 4, 5], ref_brute([1, 2, 3, 4, 5])),
    ([9, 76, 64, 21], ref_brute([9, 76, 64, 21])),
    ([3, 0, 4, 0, 5], ref_brute([3, 0, 4, 0, 5])),
    (rand_small, ref_brute(rand_small)),
    (rand_mid, ref_dp(rand_mid)),
    ([100] * 300, ref_dp([100] * 300)),
    (rand_large, ref_dp(rand_large)),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for i, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().maxCoins(list(nums))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got=exception: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)