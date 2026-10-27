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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
      "Optional": Optional, "Dict": Dict, "math": math}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]

# (x, expected)
CASES = [
    (123, 321),                 # example 1
    (-123, -321),               # example 2
    (120, 21),                  # example 3
    (0, 0),                     # zero
    (7, 7),                     # single digit
    (-5, -5),                   # single negative digit
    (1000000000, 1),            # many trailing zeros
    (-100, -1),                 # negative trailing zeros
    (1534236469, 0),            # overflow
    (2147483647, 0),            # INT_MAX overflows when reversed
    (-2147483648, 0),           # INT_MIN overflows when reversed
    (1463847412, 2147483641),   # largest-ish valid result
    (-1463847412, -2147483641), # negative near the boundary
    (1563847412, 0),            # just over INT_MAX
    (-1563847412, 0),           # just under INT_MIN
]

passed = 0
total = len(CASES)
for n, (x, expected) in enumerate(CASES, 1):
    try:
        got = Solution().reverse(x)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={x}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={x}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)