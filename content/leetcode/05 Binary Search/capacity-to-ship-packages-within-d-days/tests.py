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


def tree_to_py(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

CASES = [
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15),
    (([3, 2, 2, 4, 1, 4], 3), 6),
    (([1, 2, 3, 1, 1], 4), 3),
    (([5], 1), 5),
    (([1, 1, 1, 1], 1), 4),
    (([1, 1, 1, 1], 4), 1),
    (([10, 50, 100, 100, 50, 100, 100, 100], 5), 160),
    (([2, 3, 5], 2), 5),
    (([1, 2, 3, 4, 5], 2), 9),
    (([7, 2, 5, 10, 8], 2), 18),
    (([500] * 50000, 50000), 500),
    (([500] * 50000, 1), 25000000),
    (([1] * 50000, 2), 25000),
    (([500] * 50000, 25000), 1000),
]


def run():
    passed = 0
    total = len(CASES)
    for n, (args, expected) in enumerate(CASES, 1):
        weights, days = args
        shown = (weights if len(weights) <= 20 else f"<{len(weights)} items>", days)
        try:
            sol = ns["Solution"]()
            got = sol.shipWithinDays(list(weights), days)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got=error: {e!r}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()
