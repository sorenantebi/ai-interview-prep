import sys
import math
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
      "Optional": Optional, "Dict": Dict, "math": math}
exec(open("attempt.py").read(), ns)

cases = [
    ([3, 6, 7, 11], 8, 4),
    ([30, 11, 23, 4, 20], 5, 30),
    ([30, 11, 23, 4, 20], 6, 23),
    ([1], 1, 1),
    ([10], 1, 10),
    ([10], 5, 2),
    ([1, 1, 1, 1], 4, 1),
    ([5, 5, 5, 5], 8, 3),
    ([10**9], 2, 5 * 10**8),
    ([10**9] * 10000, 10**9, 10000),
    ([10**9, 10**9], 3, 10**9),
    ([312884470], 312884469, 2),
    ([2, 2], 3, 2),
    ([1, 2, 3, 4, 5], 15, 1),
    ([9, 9, 9], 4, 9),
]

passed = 0
total = len(cases)
for i, (piles, h, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().minEatingSpeed(list(piles), h)
        if got == expected:
            passed += 1
            print(f"PASS case {i}")
        else:
            shown = piles if len(piles) <= 10 else f"<{len(piles)} piles>"
            print(f"FAIL case {i}: input=piles={shown}, h={h}, expected={expected}, got={got}")
    except Exception as e:
        shown = piles if len(piles) <= 10 else f"<{len(piles)} piles>"
        print(f"FAIL case {i}: input=piles={shown}, h={h}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
