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

big_n = 20000

cases = [
    # (bookings, n, expected)
    ([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5, [10, 55, 45, 25, 25]),
    ([[1, 2, 10], [2, 2, 15]], 2, [10, 25]),
    ([[1, 1, 5]], 1, [5]),
    ([[1, 1, 3], [1, 1, 4]], 1, [7]),
    ([[1, 5, 2]], 5, [2, 2, 2, 2, 2]),
    ([[3, 4, 7]], 4, [0, 0, 7, 7]),
    ([[1, 1, 1], [4, 4, 2]], 5, [1, 0, 0, 2, 0]),
    ([[1, 2, 3], [3, 4, 5]], 4, [3, 3, 5, 5]),
    ([[1, 6, 1], [2, 5, 2], [3, 4, 3]], 6, [1, 3, 6, 6, 3, 1]),
    ([[1, big_n, 10000]] * 20000, big_n, [200000000] * big_n),
    ([[i, i, 1] for i in range(1, big_n + 1)], big_n, [1] * big_n),
    ([[i, big_n, 1] for i in range(1, big_n + 1)], big_n, list(range(1, big_n + 1))),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(cases)
for idx, (bookings, n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().corpFlightBookings([list(b) for b in bookings], n)
        if list(got) == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=({short(bookings)}, {n}), expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({short(bookings)}, {n}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
