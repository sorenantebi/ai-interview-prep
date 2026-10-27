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

# large matrix: 100 x 100, strictly increasing by 2 (all even values), range stays within constraints
big = [[(r * 100 + c) * 2 - 10000 + 1 for c in range(100)] for r in range(100)]
# values: odd numbers from -9999 to 9999 -> evens are absent

cases = [
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13, False),
    ([[1]], 1, True),
    ([[1]], 2, False),
    ([[1, 3, 5, 7, 9]], 7, True),
    ([[1], [3], [5], [7]], 5, True),
    ([[1], [3], [5], [7]], 4, False),
    ([[-9, -7, -5], [-3, -1, 0], [2, 4, 6]], -3, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 0, False),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 61, False),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60, True),
    ([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 8, False),
    (big, big[99][99], True),
    (big, big[57][31], True),
    (big, big[57][31] + 1, False),
]

passed = 0
total = len(cases)
for i, (matrix, target, expected) in enumerate(cases, 1):
    shown = matrix if len(matrix) * len(matrix[0]) <= 20 else f"<{len(matrix)}x{len(matrix[0])} matrix>"
    try:
        got = ns["Solution"]().searchMatrix([row[:] for row in matrix], target)
        if bool(got) == expected and isinstance(got, bool):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=({shown}, {target}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=({shown}, {target}), expected={expected}, got=exception: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)