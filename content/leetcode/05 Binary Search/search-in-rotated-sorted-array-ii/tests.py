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
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


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

big_dup = [1] * 2500 + [2] + [1] * 2499
big_distinct_sorted = list(range(-2500, 2500))
big_rot = big_distinct_sorted[1234:] + big_distinct_sorted[:1234]

cases = [
    ([2, 5, 6, 0, 0, 1, 2], 0, True),
    ([2, 5, 6, 0, 0, 1, 2], 3, False),
    ([1], 1, True),
    ([1], 0, False),
    ([1, 0, 1, 1, 1], 0, True),
    ([1, 1, 1, 1, 1, 1, 2, 1, 1], 2, True),
    ([1, 1, 1, 1, 1, 1, 2, 1, 1], 3, False),
    ([-3, -1, 0, 2, -10, -8, -5], -8, True),
    ([-3, -1, 0, 2, -10, -8, -5], -2, False),
    ([3, 1], 1, True),
    ([2, 2, 2, 2], 3, False),
    ([1, 3, 1, 1, 1], 3, True),
    ([4, 5, 6, 7, 0, 1, 2], 0, True),
    (big_dup, 2, True),
    (big_dup, 3, False),
    (big_rot, 2499, True),
    (big_rot, 2500, False),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for i, (nums, target, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().search(list(nums), target)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            print(f"FAIL case {i}: input=({short(nums)}, {target}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=({short(nums)}, {target}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)