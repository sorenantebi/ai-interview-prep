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


def tree_to_array(root):
    out = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

BIG = 10 ** 9

cases = [
    ([8, 2, 4, 7], 4, 2),
    ([10, 1, 2, 4, 7, 2], 5, 4),
    ([4, 2, 2, 2, 4, 4, 2, 2], 0, 3),
    ([5], 0, 1),
    ([1, 1, 1, 1], 0, 4),
    ([1, 2, 3, 4, 5], 0, 1),
    ([1, 5, 6, 7, 8, 10, 6, 5, 6], 4, 5),
    ([1, 2, 3, 4, 5], BIG, 5),
    ([BIG, 1, BIG, 1], BIG - 1, 4),
    ([BIG, 1, BIG, 1], BIG - 2, 1),
    ([2, 2, 2, 3, 3, 3, 3, 2], 1, 8),
    ([3, 1, 4, 1, 5, 9, 2, 6], 3, 4),
    (list(range(1, 100001)), 10, 11),
    ([1, BIG] * 50000, BIG - 1, 100000),
    (list(range(100000, 0, -1)), 0, 1),
]

passed = 0
total = len(cases)
for i, (nums, limit, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().longestSubarray(list(nums), limit)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
            print(f"FAIL case {i}: input=({shown}, {limit}), expected={expected}, got={got}")
    except Exception as e:
        shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
        print(f"FAIL case {i}: input=({shown}, {limit}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
