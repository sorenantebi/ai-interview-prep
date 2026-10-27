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


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
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
    s = sorted(set(nums))
    if not s:
        return 0
    best = cur = 1
    for a, b in zip(s, s[1:]):
        cur = cur + 1 if b == a + 1 else 1
        best = max(best, cur)
    return best


random.seed(12345)
big_shuffled = list(range(100000))
random.shuffle(big_shuffled)
big_random = [random.randint(-10**9, 10**9) for _ in range(100000)]
big_dups = [5] * 100000
big_two_runs = list(range(-50000, 0)) + list(range(10**9 - 49999, 10**9 + 1))
random.shuffle(big_two_runs)

cases = [
    ([100, 4, 200, 1, 3, 2], 4),
    ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
    ([1, 0, 1, 2], 3),
    ([], 0),
    ([7], 1),
    ([5, 5, 5, 5], 1),
    ([-3, -2, -1, 0, 1], 5),
    ([-10**9, 10**9], 1),
    ([10**9, 10**9 - 1, 10**9 - 2, -10**9, -10**9 + 1], 3),
    ([1, 3, 5, 7, 9], 1),
    ([9, 8, 7, 6, 5, 4, 3, 2, 1], 9),
    (big_shuffled, 100000),
    (big_random, brute(big_random)),
    (big_dups, 1),
    (big_two_runs, 50000),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
for i, (nums, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.longestConsecutive(list(nums))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)