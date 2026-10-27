import sys
import math
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
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


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


def close(a, b):
    return math.isclose(a, b, rel_tol=1e-5, abs_tol=1e-5)


# (x, n, expected)
cases = [
    (2.0, 10, 1024.0),
    (2.1, 3, 9.261),
    (2.0, -2, 0.25),
    (5.0, 0, 1.0),
    (0.0, 5, 0.0),
    (1.0, 2**31 - 1, 1.0),
    (1.0, -2**31, 1.0),
    (-1.0, 2**31 - 1, -1.0),
    (-1.0, -2**31, 1.0),
    (-2.0, 3, -8.0),
    (-2.0, -3, -0.125),
    (2.0, -2**31, 0.0),
    (0.5, 10, 0.5 ** 10),
    (1.0000001, 100000, 1.0000001 ** 100000),
    (0.99999, 2**31 - 1, 0.0),
    (10.0, 4, 10000.0),
]

passed = 0
total = len(cases)
for i, (x, n, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.myPow(x, n)
        if close(got, expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=(x={x}, n={n}), expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input=(x={x}, n={n}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)