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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([3, 2, 3], 3),
    ([2, 2, 1, 1, 1, 2, 2], 2),
    ([1], 1),
    ([5, 5], 5),
    ([-1, -1, 2], -1),
    ([1, 2, 1, 2, 1], 1),
    ([1, 1, 2, 2, 2], 2),
    ([0, 0, 0, 0, 1, 2, 3], 0),
    ([-10**9] * 3 + [10**9] * 2, -10**9),
    ([10**9, -10**9, 10**9, -10**9, 10**9], 10**9),
    # large: majority 7 interleaved with distinct others (25001 vs 24999)
    ([7 if i % 2 == 0 else 100 + i for i in range(49999)] + [7], 7),
    # large: majority at the end after many distinct values (25001 vs 24999)
    ([-i - 1 for i in range(24999)] + [42] * 25001, 42),
]


def show(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().majorityElement(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={show(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={show(nums)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)