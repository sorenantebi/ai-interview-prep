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

BIG = 10**9

cases = [
    # (rectangles, expected)
    ([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]], 6),
    ([[0, 0, BIG, BIG]], 49),
    ([[0, 0, 1, 1]], 1),
    ([[0, 0, 1, 1], [2, 2, 4, 4]], 5),
    ([[0, 0, 3, 3], [0, 0, 3, 3]], 9),
    ([[0, 0, 4, 4], [1, 1, 2, 2]], 16),
    ([[0, 0, 1, 2], [1, 0, 2, 2]], 4),
    ([[0, 1, 3, 2], [1, 0, 2, 3]], 5),
    ([[0, 0, BIG, BIG], [BIG // 2, BIG // 2, BIG, BIG]], 49),
    ([[0, 0, BIG, 1], [0, 2, BIG, 3]], 999999993),
    ([[i, i, i + 2, i + 2] for i in range(200)], 601),
    ([[0, 0, i + 1, i + 1] for i in range(200)], 40000),
]

passed = 0
total = len(cases)
for n, (rects, expected) in enumerate(cases, 1):
    try:
        inp = [list(r) for r in rects]
        got = ns["Solution"]().rectangleArea(inp)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            s = str(rects)
            if len(s) > 200:
                s = s[:200] + "..."
            print(f"FAIL case {n}: input={s}, expected={expected}, got={got}")
    except Exception as e:
        s = str(rects)
        if len(s) > 200:
            s = s[:200] + "..."
        print(f"FAIL case {n}: input={s}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
