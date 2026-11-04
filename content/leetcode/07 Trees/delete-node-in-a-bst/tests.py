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


def serialize(root):
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


def inorder(root):
    res = []
    stack = []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res


def build_balanced(sorted_vals):
    def go(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(sorted_vals[mid], go(lo, mid - 1), go(mid + 1, hi))
    return go(0, len(sorted_vals) - 1)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

BIG = list(range(-10000, 10000, 2))  # 10^4 nodes

# (name/tree builder, key, expected inorder, require identical structure)
cases = [
    # 1: example 1
    (lambda: build_tree([5, 3, 6, 2, 4, None, 7]), 3, [2, 4, 5, 6, 7], False),
    # 2: example 2, key absent
    (lambda: build_tree([5, 3, 6, 2, 4, None, 7]), 0, [2, 3, 4, 5, 6, 7], True),
    # 3: example 3, empty tree
    (lambda: build_tree([]), 0, [], True),
    # 4: single node deleted
    (lambda: build_tree([1]), 1, [], False),
    # 5: single node, key absent
    (lambda: build_tree([1]), 2, [1], True),
    # 6: delete root with two children
    (lambda: build_tree([5, 3, 6, 2, 4, None, 7]), 5, [2, 3, 4, 6, 7], False),
    # 7: delete leaf
    (lambda: build_tree([5, 3, 6, 2, 4, None, 7]), 7, [2, 3, 4, 5, 6], False),
    # 8: delete node with only a right child
    (lambda: build_tree([5, 3, 6, None, None, None, 7]), 6, [3, 5, 7], False),
    # 9: negatives, delete node with two children
    (lambda: build_tree([0, -3, 3, -5, -1, 2, 5]), -3, [-5, -1, 0, 2, 3, 5], False),
    # 10: delete root with only a left child
    (lambda: build_tree([3, 2, None, 1]), 3, [1, 2], False),
    # 11: deep successor
    (lambda: build_tree([10, 5, 20, None, None, 15, 30, 12]), 10, [5, 12, 15, 20, 30], False),
    # 12: large balanced tree, delete root-ish value
    (lambda: build_balanced(BIG), BIG[len(BIG) // 2],
     [v for v in BIG if v != BIG[len(BIG) // 2]], False),
    # 13: large tree, key absent (odd value)
    (lambda: build_balanced(BIG), 1, BIG, True),
]

passed = 0
total = len(cases)
for n, (builder, key, expected, same) in enumerate(cases, 1):
    root = builder()
    before = serialize(root)
    try:
        res = ns["Solution"]().deleteNode(root, key)
        got = inorder(res)
        ok = got == expected  # strictly increasing inorder with the right values => valid BST
        if ok and same:
            ok = serialize(res) == before
        if ok:
            passed += 1
            print(f"PASS case {n}")
        else:
            shown_in = before if len(before) <= 40 else f"<tree of {len(before)} slots>"
            shown_exp = expected if len(expected) <= 40 else f"<{len(expected)} values>"
            shown_got = got if len(got) <= 40 else f"<{len(got)} values>"
            print(f"FAIL case {n}: input={shown_in}, key={key}, expected inorder={shown_exp}"
                  f"{' (structure unchanged)' if same else ''}, got inorder={shown_got}")
    except Exception as e:
        print(f"FAIL case {n}: input key={key}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)