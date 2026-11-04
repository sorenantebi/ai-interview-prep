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

# (n, expected)
CASES = [
    (12, 3),      # example 1
    (13, 2),      # example 2
    (1, 1),       # minimum
    (2, 2),       # 1+1
    (3, 3),       # 1+1+1
    (4, 1),       # perfect square
    (7, 4),       # 4+1+1+1
    (8, 2),       # 4+4
    (99, 3),      # 49+49+1
    (28, 4),      # 4*7 form
    (5000, 2),    # 70^2 + 10^2
    (9999, 4),    # 8b+7 form, large
    (10000, 1),   # 100^2, max
]

passed = 0
total = len(CASES)
for idx, (n, expected) in enumerate(CASES, 1):
    try:
        got = ns["Solution"]().numSquares(n)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={n}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={n}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)