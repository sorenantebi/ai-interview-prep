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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
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


def expected_bits(n):
    return [bin(i).count("1") for i in range(n + 1)]


cases = [
    (2, [0, 1, 1]),
    (5, [0, 1, 1, 2, 1, 2]),
    (0, [0]),
    (1, [0, 1]),
    (3, [0, 1, 1, 2]),
    (7, expected_bits(7)),
    (8, expected_bits(8)),
    (15, expected_bits(15)),
    (16, expected_bits(16)),
    (31, expected_bits(31)),
    (1000, expected_bits(1000)),
    (65535, expected_bits(65535)),
    (100000, expected_bits(100000)),
]


def fmt(x):
    s = repr(x)
    return s if len(s) < 200 else s[:200] + "..."


passed = 0
total = len(cases)
for idx, (n, exp) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().countBits(n)
        got = list(got)
        if got == exp:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=n={n}, expected={fmt(exp)}, got={fmt(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input=n={n}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)