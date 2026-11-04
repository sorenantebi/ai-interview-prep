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
    ([1, 5, 6, 2], 1),
    ([1, 2, 3, 6, 5, 4], 3),
    ([1, 3, 3, 3, 2, 4, 2, 1, 2], 4),
    ([1], 0),
    ([5, 5, 5, 5], 0),
    (list(range(1, 11)), 0),
    ([5, 4, 3, 2, 1], 0),
    ([100000, 1, 50000], 1),
    ([1, 3, 2], 1),
    ([4, 2, 6, 1, 3, 5, 7], 3),
    ([1] * 30000 + [100000] * 30000 + [50000] * 40000, 199999993),
    (list(range(1, 100001)), 0),
]


def short(x):
    s = repr(x)
    return s if len(s) < 200 else s[:200] + "..."


passed = 0
for n, (inp, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().createSortedArray(list(inp))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(inp)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)