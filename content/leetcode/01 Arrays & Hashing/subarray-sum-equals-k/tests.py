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


def list_to_py(node):
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


def tree_to_py(root):
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

cases = [
    ([1, 1, 1], 2, 2),
    ([1, 2, 3], 3, 2),
    ([1], 1, 1),
    ([1], 0, 0),
    ([0, 0, 0], 0, 6),
    ([-1, -1, 1], 0, 1),
    ([1, -1, 0], 0, 3),
    ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
    ([-1, -2, -3], -3, 2),
    ([1, 2, 1, 2, 1], 3, 4),
    ([1, 2, 3], 10000000, 0),
    ([0] * 20000, 0, 200010000),
    ([1] * 20000, 10000, 10001),
]

passed = 0
total = len(cases)
for idx, (nums, k, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().subarraySum(list(nums), k)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=({shown}, {k}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({shown}, {k}), expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)