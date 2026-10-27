import sys
from typing import List, Optional, Dict
from collections import deque


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


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def bst_from_sorted(vals):
    """Balanced BST from sorted distinct values, returned as TreeNode."""
    def rec(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(vals[mid], rec(lo, mid - 1), rec(mid + 1, hi))
    return rec(0, len(vals) - 1)


def left_chain(n):
    # root n, left child n-1, ... 1  (values 1..n)
    root = None
    for v in range(1, n + 1):
        root = TreeNode(v, root, None)
    return root


def right_chain(n):
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, None, root)
    return root


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    # (description for printing, tree builder, k, expected)
    ([3, 1, 4, None, 2], lambda: build_tree([3, 1, 4, None, 2]), 1, 1),
    ([5, 3, 6, 2, 4, None, None, 1], lambda: build_tree([5, 3, 6, 2, 4, None, None, 1]), 3, 3),
    ([1], lambda: build_tree([1]), 1, 1),
    ([0], lambda: build_tree([0]), 1, 0),
    ([2, 1, 3], lambda: build_tree([2, 1, 3]), 3, 3),
    ([2, 1, 3], lambda: build_tree([2, 1, 3]), 2, 2),
    ([5, 3, 6, 2, 4, None, None, 1], lambda: build_tree([5, 3, 6, 2, 4, None, None, 1]), 6, 6),
    ("left chain 1..50", lambda: left_chain(50), 50, 50),
    ("right chain 1..50", lambda: right_chain(50), 1, 1),
    ("right chain 1..50", lambda: right_chain(50), 37, 37),
    ("balanced 0..9999", lambda: bst_from_sorted(list(range(10000))), 1, 0),
    ("balanced 0..9999", lambda: bst_from_sorted(list(range(10000))), 10000, 9999),
    ("balanced 0..9999", lambda: bst_from_sorted(list(range(10000))), 5000, 4999),
    ("left chain 1..5000", lambda: left_chain(5000), 2500, 2500),
]

sys.setrecursionlimit(100000)

passed = 0
total = len(cases)
for i, (desc, builder, k, expected) in enumerate(cases, 1):
    try:
        root = builder()
        got = ns["Solution"]().kthSmallest(root, k)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={desc}, k={k}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={desc}, k={k}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)