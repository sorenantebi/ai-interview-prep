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


def run(nums):
    return ns["Solution"]().missingNumber(nums)


def make_large(n, missing, seed):
    vals = [v for v in range(n + 1) if v != missing]
    random.Random(seed).shuffle(vals)
    return vals


cases = [
    ([3, 0, 1], 2),
    ([0, 1], 2),
    ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
    ([0], 1),
    ([1], 0),
    ([1, 2], 0),
    ([0, 2], 1),
    ([0, 1, 2, 3, 4], 5),
    ([5, 4, 3, 2, 1], 0),
    (make_large(10000, 0, 1), 0),
    (make_large(10000, 10000, 2), 10000),
    (make_large(10000, 4567, 3), 4567),
]

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
    try:
        got = run(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)