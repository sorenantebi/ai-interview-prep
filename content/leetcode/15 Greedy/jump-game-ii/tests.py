import sys
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


def reference(nums):
    n = len(nums)
    jumps = cur_end = farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps


def make_large_ones(n):
    return [1] * n


def make_large_big(n):
    return [1000] * n


def make_pseudo_random(n):
    seed = 12345
    arr = []
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        arr.append(1 + seed % 50)
    return arr


cases = [
    ([2, 3, 1, 1, 4], 2),
    ([2, 3, 0, 1, 4], 2),
    ([0], 0),
    ([1], 0),
    ([1, 2], 1),
    ([5, 0, 0, 0, 0, 0], 1),
    ([1, 1, 1, 1], 3),
    ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 1),
    ([1, 2, 3, 4, 5], 3),
    ([2, 1], 1),
    ([1, 3, 1, 1, 1, 1], 3),
    (make_large_ones(10000), 9999),
    (make_large_big(10000), None),
    (make_pseudo_random(10000), None),
]

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(nums)
    shown = nums if len(nums) <= 20 else f"<list of length {len(nums)}>"
    try:
        sol = ns["Solution"]()
        got = sol.jump(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=Exception({e})")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)