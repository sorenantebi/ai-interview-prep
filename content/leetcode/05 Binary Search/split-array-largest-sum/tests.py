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
    ([7, 2, 5, 10, 8], 2, 18),
    ([1, 2, 3, 4, 5], 2, 9),
    ([1], 1, 1),
    ([0, 0, 0], 2, 0),
    ([1, 2, 3, 4, 5], 1, 15),
    ([1, 2, 3, 4, 5], 5, 5),
    ([1, 4, 4], 3, 4),
    ([2, 3, 1, 2, 4, 3], 3, 6),
    ([10, 5, 13, 4, 8, 4, 5, 11, 14, 9, 16, 10, 20, 8], 8, 25),
    ([1000000] * 1000, 50, 20000000),
    ([1] * 1000, 7, 143),
    ([5, 0, 0, 5], 2, 5),
    ([1, 1000000], 2, 1000000),
    ([1, 2, 3, 4, 5], 3, 6),
]

passed = 0
for idx, (nums, k, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
    try:
        got = ns["Solution"]().splitArray(list(nums), k)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=({shown}, {k}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({shown}, {k}), expected={expected}, got=error: {e!r}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
