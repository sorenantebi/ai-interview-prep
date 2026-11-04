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


def list_to_py(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ([1, -2, 3, -2], 3),
    ([5, -3, 5], 10),
    ([-3, -2, -3], -2),
    ([5], 5),
    ([-7], -7),
    ([3, -1, 2, -1], 4),
    ([8, -1, -1, -1, 8], 16),
    ([1, 2, 3, 4], 10),
    ([-1, -1], -1),
    ([0, 0, 0], 0),
    ([-2, 4, -5, 4, -5, 9, 4], 15),
    ([2, -2, 2, 7, 8, 0], 19),
    ([30000] * 30000, 900000000),
    ([-1] * 15000 + [1] * 15000, 15000),
    ([1] * 15000 + [-1] * 15000, 15000),
]

passed = 0
total = len(cases)
for idx, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().maxSubarraySumCircular(list(nums))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown = nums if len(nums) <= 20 else f"<list of length {len(nums)}>"
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        shown = nums if len(nums) <= 20 else f"<list of length {len(nums)}>"
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
