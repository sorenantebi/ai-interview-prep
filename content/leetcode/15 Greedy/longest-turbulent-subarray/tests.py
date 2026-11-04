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
    ([9, 4, 2, 10, 7, 8, 8, 1, 9], 5),
    ([4, 8, 12, 16], 2),
    ([100], 1),
    ([5, 5, 5, 5], 1),
    ([1, 2], 2),
    ([2, 1], 2),
    ([3, 3], 1),
    ([1, 2, 1, 2, 1, 2], 6),
    ([0, 1, 1, 0, 1, 0, 1, 1, 0], 5),
    ([1, 1, 2, 3, 2, 1], 3),
    ([9, 9, 9, 1, 2, 1], 4),
    ([10, 9, 8, 7], 2),
    ([i % 2 for i in range(40000)], 40000),
    (list(range(40000)), 2),
    ([i % 2 for i in range(30000)] + [1] + [i % 2 for i in range(5000)], 30000),
]

passed = 0
total = len(cases)
for n, (arr, expected) in enumerate(cases, 1):
    shown = arr if len(arr) <= 20 else f"<list of length {len(arr)}>"
    try:
        got = ns["Solution"]().maxTurbulenceSize(list(arr))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, expected={expected}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
