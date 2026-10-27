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


def list_to_array(node):
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

big = list(range(-4999, 5001))  # 10^4 distinct values within (-10^4, 10^4)

cases = [
    ([-1, 0, 3, 5, 9, 12], 9, 4),
    ([-1, 0, 3, 5, 9, 12], 2, -1),
    ([5], 5, 0),
    ([5], -5, -1),
    ([5], 9999, -1),
    ([1, 3], 1, 0),
    ([1, 3], 3, 1),
    ([1, 3], 2, -1),
    ([-1, 0, 3, 5, 9, 12], -1, 0),
    ([-1, 0, 3, 5, 9, 12], 12, 5),
    ([-9999, -5, -1, 0], -5, 1),
    ([-9999, -5, -1, 0], -10000 + 1 - 1 + 0 - 0 + 2, -1),
    (big, 5000, len(big) - 1),
    (big, -4999, 0),
    (big, 0, 4999),
    (big, 9999, -1),
]

passed = 0
total = len(cases)
for n, (nums, target, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().search(list(nums), target)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
            print(f"FAIL case {n}: input=(nums={shown}, target={target}), expected={expected}, got={got}")
    except Exception as e:
        shown = nums if len(nums) <= 20 else f"<list of {len(nums)}>"
        print(f"FAIL case {n}: input=(nums={shown}, target={target}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
