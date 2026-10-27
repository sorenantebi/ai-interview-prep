import sys
from typing import List, Optional, Dict
from collections import deque

sys.setrecursionlimit(20000)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """Build a tree from a LeetCode-style level-order list (None = missing)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


def serialize_tree(root):
    """Serialize a tree to a LeetCode-style level-order list."""
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


def build_chain(vals, side="left"):
    """Build a degenerate tree following vals along one side."""
    root = None
    for v in reversed(vals):
        node = TreeNode(v)
        if side == "left":
            node.left = root
        else:
            node.right = root
        root = node
    return root


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(%d chars)" % len(s)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]

# (description, builder returning (root, subRoot), expected)
cases = [
    ("root=[3,4,5,1,2], subRoot=[4,1,2]",
     lambda: (build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 2])), True),
    ("root=[3,4,5,1,2,null,null,null,null,0], subRoot=[4,1,2]",
     lambda: (build_tree([3, 4, 5, 1, 2, None, None, None, None, 0]), build_tree([4, 1, 2])), False),
    ("root=[1], subRoot=[1]",
     lambda: (build_tree([1]), build_tree([1])), True),
    ("root=[1], subRoot=[2]",
     lambda: (build_tree([1]), build_tree([2])), False),
    ("root=[1,1], subRoot=[1] (leaf match)",
     lambda: (build_tree([1, 1]), build_tree([1])), True),
    ("root=[1,null,1], subRoot=[1,1] (left vs right child)",
     lambda: (build_tree([1, None, 1]), build_tree([1, 1])), False),
    ("root=[-1,-2,-3], subRoot=[-3]",
     lambda: (build_tree([-1, -2, -3]), build_tree([-3])), True),
    ("root=[3,4,5,1,2], subRoot=[4,2,1] (swapped children)",
     lambda: (build_tree([3, 4, 5, 1, 2]), build_tree([4, 2, 1])), False),
    ("root=[3,4,5,1,2], subRoot=[3,4,5,1,2] (whole tree)",
     lambda: (build_tree([3, 4, 5, 1, 2]), build_tree([3, 4, 5, 1, 2])), True),
    ("root=[1], subRoot=[1,2] (subRoot larger)",
     lambda: (build_tree([1]), build_tree([1, 2])), False),
    ("root=[1,1,1,1,null,null,null,1], subRoot=[1,1] (duplicates, deep match)",
     lambda: (build_tree([1, 1, 1, 1, None, None, None, 1]), build_tree([1, 1])), True),
    ("root=[10000,-10000], subRoot=[-10000] (value bounds)",
     lambda: (build_tree([10000, -10000]), build_tree([-10000])), True),
    ("large: left chain of 2000 ones, subRoot chain of 1000 ones",
     lambda: (build_chain([1] * 2000), build_chain([1] * 1000)), True),
    ("large: left chain of 2000 ones, subRoot chain of 999 ones then 2",
     lambda: (build_chain([1] * 2000), build_chain([1] * 999 + [2])), False),
]

passed = 0
total = len(cases)
for n, (desc, builder, expected) in enumerate(cases, 1):
    try:
        root, sub = builder()
        got = Solution().isSubtree(root, sub)
        if got == expected and isinstance(got, bool):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(desc)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(desc)}, expected={expected}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)