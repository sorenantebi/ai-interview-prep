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
    out, queue = [], [root]
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


def brute(nums):
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        ok = True
        total = 0
        for i in range(n):
            if mask >> i & 1:
                if n > 1 and mask >> ((i + 1) % n) & 1:
                    ok = False
                    break
                total += nums[i]
        if ok:
            best = max(best, total)
    return best


rng = random.Random(1234)
rand_small = [rng.randint(0, 1000) for _ in range(12)]
rand_small2 = [rng.randint(0, 20) for _ in range(13)]

cases = [
    ([2, 3, 2], 3),
    ([1, 2, 3, 1], 4),
    ([1, 2, 3], 3),
    ([5], 5),
    ([0], 0),
    ([1, 2], 2),
    ([2, 1, 1, 2], 3),
    ([0, 0, 0, 0], 0),
    ([200, 3, 140, 20, 10], 340),
    ([1, 3, 1, 3, 100], 103),
    (rand_small, brute(rand_small)),
    (rand_small2, brute(rand_small2)),
    ([1000] * 100, 50000),
]

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().rob(list(nums))
        if got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)