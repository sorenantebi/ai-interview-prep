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
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


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


def reference(nums):
    rob1, rob2 = 0, 0
    for n in nums:
        temp = max(n + rob1, rob2)
        rob1 = rob2
        rob2 = temp
    return rob2


def brute(nums):
    best = 0
    n = len(nums)
    for mask in range(1 << n):
        if mask & (mask >> 1):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best


random.seed(12345)
small_random = [random.randint(0, 400) for _ in range(12)]
large_random = [random.randint(0, 400) for _ in range(100)]

cases = [
    ([1, 2, 3, 1], 4),
    ([2, 7, 9, 3, 1], 12),
    ([5], 5),
    ([0], 0),
    ([1, 2], 2),
    ([2, 1], 2),
    ([0, 0, 0, 0], 0),
    ([400] * 100, 400 * 50),
    ([5, 5, 5, 5, 5], 15),
    ([2, 1, 1, 2], 4),
    ([100, 1, 1, 100, 1, 1, 100], 300),
    (list(range(1, 101)), reference(list(range(1, 101)))),
    (small_random, brute(small_random)),
    (large_random, reference(large_random)),
]


def run():
    passed = 0
    total = len(cases)
    for idx, (nums, expected) in enumerate(cases, 1):
        inp = list(nums)
        try:
            got = ns["Solution"]().rob(list(nums))
            if got == expected:
                print(f"PASS case {idx}")
                passed += 1
            else:
                print(f"FAIL case {idx}: input={inp}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {idx}: input={inp}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()