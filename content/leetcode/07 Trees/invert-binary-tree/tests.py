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


def build_tree(vals):
    """Build a tree from a LeetCode level-order list (None for missing)."""
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


def serialize_tree(root):
    """Serialize to LeetCode level-order list, trimming trailing None."""
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


def mirror_list(vals):
    """Reference: mirror a tree given as a list, via independent recursion."""
    root = build_tree(vals)

    def rec(n):
        if n is None:
            return None
        return TreeNode(n.val, rec(n.right), rec(n.left))

    return serialize_tree(rec(root))


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def skewed(n, side):
    root = TreeNode(0)
    cur = root
    for i in range(1, n):
        nxt = TreeNode(i % 100)
        if side == "left":
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return serialize_tree(root)


cases = [
    ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),
    ([2, 1, 3], [2, 3, 1]),
    ([], []),
    ([1], [1]),
    ([1, 2], [1, None, 2]),
    ([1, None, 2], [1, 2]),
    ([1, 2, None, 3], [1, None, 2, None, 3]),
    ([-1, -2, -3], [-1, -3, -2]),
    ([5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]),
    ([1, 2, 3, None, 4, 5], [1, 3, 2, None, 5, 4]),
    ([-100, 100, None, -100], [-100, None, 100, None, -100]),
]

# large inputs: 100-node skewed trees (performance / depth)
big_left = skewed(100, "left")
big_right = skewed(100, "right")
cases.append((big_left, mirror_list(big_left)))
cases.append((big_right, mirror_list(big_right)))

# full-ish tree with 100 nodes
full = list(range(1, 101))
cases.append((full, mirror_list(full)))

passed = 0
total = len(cases)
for idx, (inp, expected) in enumerate(cases, 1):
    try:
        got = serialize_tree(Solution().invertTree(build_tree(inp)))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={inp}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={inp}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)