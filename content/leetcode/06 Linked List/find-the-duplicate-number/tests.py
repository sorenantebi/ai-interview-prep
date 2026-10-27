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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
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


def make_large(n, dup, copies, seed):
    rng = random.Random(seed)
    others = [v for v in range(1, n + 1) if v != dup]
    rng.shuffle(others)
    arr = [dup] * copies + others[: n + 1 - copies]
    rng.shuffle(arr)
    return arr


cases = [
    ([1, 3, 4, 2, 2], 2),
    ([3, 1, 3, 4, 2], 3),
    ([3, 3, 3, 3, 3], 3),
    ([1, 1], 1),
    ([1, 1, 2], 1),
    ([2, 2, 1], 2),
    ([2, 1, 2], 2),
    ([1, 2, 3, 4, 5, 5], 5),
    ([2, 2, 2, 2, 2], 2),
    ([1, 4, 4, 2, 4], 4),
    (make_large(100000, 54321, 2, 1), 54321),
    (make_large(100000, 1, 5, 2), 1),
    (make_large(100000, 100000, 3, 3), 100000),
    ([100000] * 100001, 100000),
]

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of length {len(nums)}>"
    try:
        original = list(nums)
        got = ns["Solution"]().findDuplicate(nums)
        if nums != original:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got} (input was modified)")
        elif got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)