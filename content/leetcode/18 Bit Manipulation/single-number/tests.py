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


def make_large():
    rng = random.Random(12345)
    vals = rng.sample(range(-30000, 30001), 15000)
    single = vals[0]
    nums = vals[1:] * 2 + [single]
    rng.shuffle(nums)
    return nums, single


large_nums, large_single = make_large()

# worst-case size with a single at an extreme value
extreme = list(range(-14999, 15000))
extreme_nums = extreme * 2 + [-30000]
random.Random(7).shuffle(extreme_nums)

cases = [
    ([2, 2, 1], 1),
    ([4, 1, 2, 1, 2], 4),
    ([1], 1),
    ([-1], -1),
    ([0], 0),
    ([0, 0, 5], 5),
    ([-3, -3, -7], -7),
    ([-1, 1, -1], 1),
    ([7, 3, 7, 3, 9, 9, -4], -4),
    ([30000, -30000, 30000], -30000),
    ([5, 5, 5, 5, 8, 5, 5], 8),
    (large_nums, large_single),
    (extreme_nums, -30000),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for i, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().singleNumber(list(nums))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(nums)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)