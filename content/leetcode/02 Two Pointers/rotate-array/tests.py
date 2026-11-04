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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

BIG_N = 100000
BIG_K = 77777
BIG_INPUT = list(range(BIG_N))
BIG_EXPECTED = BIG_INPUT[-BIG_K:] + BIG_INPUT[:-BIG_K]

CASES = [
    ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
    ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
    ([1], 0, [1]),
    ([1], 5, [1]),
    ([1, 2], 3, [2, 1]),
    ([1, 2, 3], 0, [1, 2, 3]),
    ([1, 2, 3], 3, [1, 2, 3]),
    ([1, 2, 3], 4, [3, 1, 2]),
    ([1, 1, 2, 2, 3], 2, [2, 3, 1, 1, 2]),
    ([-2147483648, 2147483647, 0], 1, [0, -2147483648, 2147483647]),
    ([1, 2, 3, 4, 5, 6], 4, [3, 4, 5, 6, 1, 2]),
    (BIG_INPUT, BIG_K, BIG_EXPECTED),
    (list(range(BIG_N)), 100000, list(range(BIG_N))),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 120 else s[:117] + "..."


passed = 0
total = len(CASES)
for i, (nums, k, expected) in enumerate(CASES, 1):
    arr = list(nums)
    try:
        sol = ns["Solution"]()
        sol.rotate(arr, k)
        if arr == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short((nums, k))}, expected={short(expected)}, got={short(arr)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short((nums, k))}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
