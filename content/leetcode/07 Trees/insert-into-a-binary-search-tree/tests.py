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


def serialize_tree(root):
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
    def rec(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(sorted_vals[mid], rec(lo, mid - 1), rec(mid + 1, hi))
    return rec(0, len(sorted_vals) - 1)


def right_chain(n):
    root = TreeNode(1)
    cur = root
    for v in range(2, n + 1):
        cur.right = TreeNode(v)
        cur = cur.right
    return root


def left_chain(n):
    root = TreeNode(n)
    cur = root
    for v in range(n - 1, 0, -1):
        cur.left = TreeNode(v)
        cur = cur.left
    return root


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big_vals = list(range(0, 20000, 2))  # 10000 even numbers

# (builder, val, expected inorder, display of input)
cases = [
    (lambda: build_tree([4, 2, 7, 1, 3]), 5, [1, 2, 3, 4, 5, 7],
     "root=[4,2,7,1,3], val=5"),
    (lambda: build_tree([40, 20, 60, 10, 30, 50, 70]), 25, [10, 20, 25, 30, 40, 50, 60, 70],
     "root=[40,20,60,10,30,50,70], val=25"),
    (lambda: build_tree([4, 2, 7, 1, 3, None, None, None, None, None, None]), 5, [1, 2, 3, 4, 5, 7],
     "root=[4,2,7,1,3,null*6], val=5"),
    (lambda: build_tree([]), 5, [5],
     "root=[], val=5"),
    (lambda: build_tree([1]), 2, [1, 2],
     "root=[1], val=2"),
    (lambda: build_tree([1]), 0, [0, 1],
     "root=[1], val=0"),
    (lambda: build_tree([-5, -10, 0]), -7, [-10, -7, -5, 0],
     "root=[-5,-10,0], val=-7"),
    (lambda: build_tree([0]), -10 ** 8, [-10 ** 8, 0],
     "root=[0], val=-10^8"),
    (lambda: build_tree([0]), 10 ** 8, [0, 10 ** 8],
     "root=[0], val=10^8"),
    (lambda: build_tree([10, 5, 15, None, None, 12, 20]), 13, [5, 10, 12, 13, 15, 20],
     "root=[10,5,15,null,null,12,20], val=13"),
    (lambda: right_chain(500), 501, list(range(1, 502)),
     "right chain 1..500, val=501"),
    (lambda: left_chain(500), 0, list(range(0, 501)),
     "left chain 500..1, val=0"),
    (lambda: build_balanced(big_vals), 9999, sorted(big_vals + [9999]),
     "balanced BST of 10000 even numbers 0..19998, val=9999"),
]

passed = 0
total = len(cases)
for idx, (builder, val, expected, desc) in enumerate(cases, 1):
    try:
        root = builder()
        got_root = ns["Solution"]().insertIntoBST(root, val)
        got = inorder(got_root)
        strictly_increasing = all(got[i] < got[i + 1] for i in range(len(got) - 1))
        if got == expected and strictly_increasing:
            print(f"PASS case {idx}")
            passed += 1
        else:
            if len(expected) > 30:
                exp_s = f"inorder of {len(expected)} values"
                got_s = f"inorder of {len(got)} values"
            else:
                exp_s = f"inorder {expected}"
                got_s = f"inorder {got}, tree={serialize_tree(got_root)}"
            print(f"FAIL case {idx}: input={desc}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {idx}: input={desc}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)