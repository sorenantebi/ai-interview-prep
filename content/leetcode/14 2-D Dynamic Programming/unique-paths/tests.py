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
    ((3, 7), 28),
    ((3, 2), 3),
    ((1, 1), 1),
    ((1, 10), 1),
    ((10, 1), 1),
    ((2, 2), 2),
    ((7, 3), 28),
    ((10, 10), math.comb(18, 9)),
    ((1, 100), 1),
    ((100, 1), 1),
    ((3, 100), math.comb(101, 2)),
    ((23, 12), math.comb(33, 11)),
    ((51, 9), math.comb(58, 8)),
    ((100, 2), 100),
]

passed = 0
total = len(cases)
for idx, ((m, n), expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().uniquePaths(m, n)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=(m={m}, n={n}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input=(m={m}, n={n}), expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)