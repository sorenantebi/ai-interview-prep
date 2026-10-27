import sys
import random
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


sys.setrecursionlimit(50000)

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Codec = ns["Codec"]


def left_skewed(n):
    out = [0]
    for i in range(1, n):
        out += [i % 1000, None]
    return out


def right_skewed(n):
    out = [0]
    for i in range(1, n):
        out += [None, -(i % 1000)]
    return out


rng = random.Random(12345)
big_balanced = [rng.randint(-1000, 1000) for _ in range(10000)]

cases = [
    [1, 2, 3, None, None, 4, 5],
    [],
    [1],
    [1, 2],
    [1, None, 2],
    [-1, -2, -3],
    [1000, -1000, 1000, -1000],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, None, 0],
    [5, 4, 7, 3, None, 2, None, -1, None, 9],
    left_skewed(1500),
    right_skewed(1500),
    big_balanced,
]


def show(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for n, vals in enumerate(cases, 1):
    expected = tree_to_list(build_tree(vals))
    try:
        root = build_tree(vals)
        data = Codec().serialize(root)
        if not isinstance(data, str):
            raise TypeError("serialize must return str, got " + type(data).__name__)
        got_root = Codec().deserialize(data)
        got = tree_to_list(got_root)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={show(vals)}, expected={show(expected)}, got={show(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={show(vals)}, expected={show(expected)}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)