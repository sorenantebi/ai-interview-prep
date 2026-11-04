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


def build_list(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
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
    # (nums, k, expected)
    ([1, 2, 3, 1], 3, True),
    ([1, 0, 1, 1], 1, True),
    ([1, 2, 3, 1, 2, 3], 2, False),
    ([1], 0, False),
    ([1, 1], 0, False),
    ([1, 1], 1, True),
    ([1, 2, 1], 1, False),
    ([1, 2, 1], 2, True),
    ([-1, -1], 1, True),
    ([1, 2, 3, 4, 5], 100000, False),
    ([99, 99], 100000, True),
    ([10**9, -10**9, 10**9], 2, True),
    (list(range(100000)), 100000, False),
    (list(range(99999)) + [0], 99998, False),
    (list(range(99999)) + [0], 99999, True),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
for n, (nums, k, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().containsNearbyDuplicate(list(nums), k)
        if got == expected and isinstance(got, bool):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input=({short(nums)}, {k}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=({short(nums)}, {k}), error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)