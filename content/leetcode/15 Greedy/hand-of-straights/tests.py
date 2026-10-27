import sys
import heapq
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
      "Optional": Optional, "Dict": Dict, "heapq": heapq}
exec(open("attempt.py").read(), ns)

cases = [
    (([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), True),
    (([1, 2, 3, 4, 5], 4), False),
    (([1], 1), True),
    (([1, 1, 1], 1), True),
    (([1, 2, 3, 4], 2), True),
    (([1, 2, 4, 5], 2), True),
    (([1, 2, 3, 5], 2), False),
    (([1, 1, 2, 2, 3, 3], 3), True),
    (([1, 1, 2, 3], 2), False),
    (([0, 0, 0], 3), False),
    (([5, 4, 3, 2, 1, 0], 6), True),
    (([8, 10, 12], 3), False),
    (([1000000000, 999999999], 2), True),
    (([1, 2, 3, 3, 4, 4, 5, 6], 4), True),
    ((list(range(10000)), 10000), True),
    (([i // 2 for i in range(10000)], 2), True),
]

passed = 0
total = len(cases)
for n, (args, expected) in enumerate(cases, 1):
    try:
        hand, k = args
        got = ns["Solution"]().isNStraightHand(list(hand), k)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            shown = args if len(hand) <= 20 else (f"<list len {len(hand)}>", k)
            print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={args if len(args[0]) <= 20 else '<large>'}, error={e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)