import sys
from typing import List, Optional, Dict


class ListNode:
    def __init__(self, x=0, next=None):
        self.val = x
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(vals, pos=-1):
    """Build a singly linked list; tail connects to index pos (-1 = no cycle)."""
    if not vals:
        return None
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def list_to_array(head, limit=100000):
    out = []
    while head and len(out) < limit:
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
    out, queue = [], [root]
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
    # (vals, pos, expected)
    ([3, 2, 0, -4], 1, True),
    ([1, 2], 0, True),
    ([1], -1, False),
    ([], -1, False),
    ([1], 0, True),
    ([1, 2], -1, False),
    ([1, 2, 3, 4, 5], -1, False),
    ([1, 2, 3, 4, 5], 0, True),
    ([1, 2, 3, 4, 5], 4, True),
    ([1, 1, 1, 1], -1, False),
    ([1, 1, 1, 1], 2, True),
    ([-1, -2, -3], 1, True),
    (list(range(10000)), -1, False),
    (list(range(10000)), 0, True),
    (list(range(10000)), 9999, True),
    (list(range(10000)), 5000, True),
]

passed = 0
total = len(cases)
for n, (vals, pos, expected) in enumerate(cases, 1):
    desc = f"head={vals if len(vals) <= 20 else f'<{len(vals)} nodes>'}, pos={pos}"
    try:
        head = build_list(vals, pos)
        got = ns["Solution"]().hasCycle(head)
        if got is expected or (isinstance(got, bool) and got == expected):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={desc}, expected={expected}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
