import sys
from collections import deque
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
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_list(root):
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


def left_chain(n):
    # values 1..n, each node is the left child of the previous one
    root = TreeNode(1)
    cur = root
    for v in range(2, n + 1):
        cur.left = TreeNode(v)
        cur = cur.left
    return root


def right_chain(n):
    root = TreeNode(1)
    cur = root
    for v in range(2, n + 1):
        cur.right = TreeNode(v)
        cur = cur.right
    return root


def balanced_bst(lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    return TreeNode(mid, balanced_bst(lo, mid - 1), balanced_bst(mid + 1, hi))


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    (lambda: build_tree([1, None, 2, 3]), [1, 3, 2]),
    (lambda: build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9]), [4, 2, 6, 5, 7, 1, 3, 9, 8]),
    (lambda: build_tree([]), []),
    (lambda: build_tree([1]), [1]),
    (lambda: build_tree([-1, -2, -3]), [-2, -1, -3]),
    (lambda: build_tree([0, -100, 100, -100, 100]), [-100, -100, 100, 0, 100]),
    (lambda: build_tree([4, 2, 6, 1, 3, 5, 7]), [1, 2, 3, 4, 5, 6, 7]),
    (lambda: build_tree([1, 2, None, None, 3]), [2, 3, 1]),
    (lambda: left_chain(100), list(range(100, 0, -1))),
    (lambda: right_chain(100), list(range(1, 101))),
    (lambda: balanced_bst(1, 100), list(range(1, 101))),
]

passed = 0
total = len(cases)
for n, (make, expected) in enumerate(cases, 1):
    inp = None
    try:
        root = make()
        inp = tree_to_list(root)
        got = ns["Solution"]().inorderTraversal(root)
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={inp}, expected={expected}, got=error: {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)