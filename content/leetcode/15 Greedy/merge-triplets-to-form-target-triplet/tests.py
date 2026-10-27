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


def run(triplets, target):
    sol = ns["Solution"]()
    return sol.mergeTriplets([list(t) for t in triplets], list(target))


cases = [
    # examples
    ([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5], True),
    ([[3, 4, 5], [4, 5, 6]], [3, 2, 5], False),
    ([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5], True),
    # single triplet equal to target
    ([[1, 2, 3]], [1, 2, 3], True),
    # single triplet not equal
    ([[1, 2, 3]], [1, 2, 4], False),
    # single triplet exceeding target
    ([[2, 2, 2]], [1, 1, 1], False),
    # each coordinate from a different triplet
    ([[5, 1, 1], [1, 5, 1], [1, 1, 5]], [5, 5, 5], True),
    # one coordinate only reachable via unsafe triplet
    ([[5, 1, 1], [1, 5, 1], [1, 9, 5]], [5, 5, 5], False),
    # duplicates
    ([[1, 1, 1], [1, 1, 1], [2, 2, 2]], [2, 2, 2], True),
    # target minimal values
    ([[1, 1, 1], [1, 1, 1]], [1, 1, 1], True),
    # missing a coordinate entirely (all below target)
    ([[1, 5, 5], [2, 5, 5]], [3, 5, 5], False),
    # large input for performance: true
    ([[1, 1, 1]] * 100000 + [[1000, 1, 1], [1, 1000, 1], [1, 1, 1000]], [1000, 1000, 1000], True),
    # large input for performance: false (unsafe triplet kills last coordinate)
    ([[1000, 1000, 1]] * 100000 + [[1, 1, 1001 if False else 1]], [1000, 1000, 1000], False),
]

passed = 0
for n, (triplets, target, expected) in enumerate(cases, 1):
    shown = triplets if len(triplets) <= 10 else f"<{len(triplets)} triplets>"
    try:
        got = run(triplets, target)
        ok = got == expected
    except Exception as e:
        got = f"{type(e).__name__}: {e}"
        ok = False
    if ok:
        passed += 1
        print(f"PASS case {n}")
    else:
        print(f"FAIL case {n}: input=({shown}, {target}), expected={expected}, got={got}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)
