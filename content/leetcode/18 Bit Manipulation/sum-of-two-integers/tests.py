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
    ((1, 2), 3),
    ((2, 3), 5),
    ((-5, -7), -12),
    ((0, 0), 0),
    ((0, 7), 7),
    ((-7, 0), -7),
    ((5, -5), 0),
    ((-5, 5), 0),
    ((10, -3), 7),
    ((-10, 3), -7),
    ((3, -10), -7),
    ((1000, 1000), 2000),
    ((-1000, -1000), -2000),
    ((1000, -1000), 0),
    ((-1, 1), 0),
    ((-1, -1), -2),
]

passed = 0
total = len(cases)
for n, ((a, b), expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().getSum(a, b)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input=(a={a}, b={b}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=(a={a}, b={b}), expected={expected}, got=exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)