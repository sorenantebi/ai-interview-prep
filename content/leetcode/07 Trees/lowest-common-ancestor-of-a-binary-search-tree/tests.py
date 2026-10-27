import sys
from collections import deque
from typing import List, Optional, Dict

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


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    dq = deque([root])
    i = 1
    while dq and i < len(arr):
        node = dq.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            dq.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            dq.append(node.right)
        i += 1
    return root


def find_node(root, val):
    stack = [root]
    while stack:
        n = stack.pop()
        if n is None:
            continue
        if n.val == val:
            return n
        stack.append(n.left)
        stack.append(n.right)
    raise ValueError("value not in tree")


def build_balanced(lo, hi):
    # BST over integers lo..hi inclusive, built iteratively
    if lo > hi:
        return None
    root = TreeNode((lo + hi) // 2)
    stack = [(root, lo, hi)]
    while stack:
        node, l, h = stack.pop()
        m = node.val
        if l <= m - 1:
            node.left = TreeNode((l + m - 1) // 2)
            stack.append((node.left, l, m - 1))
        if m + 1 <= h:
            node.right = TreeNode((m + 1 + h) // 2)
            stack.append((node.right, m + 1, h))
    return root


def build_chain(vals, direction):
    root = TreeNode(vals[0])
    cur = root
    for v in vals[1:]:
        nxt = TreeNode(v)
        if direction == "left":
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


def ref_lca(root, pv, qv):
    cur = root
    while True:
        if cur.val < pv and cur.val < qv:
            cur = cur.right
        elif cur.val > pv and cur.val > qv:
            cur = cur.left
        else:
            return cur.val


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

big = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]

cases = []  # (name_input, root, pval, qval, expected)

cases.append(("root=%s p=2 q=8" % big, build_tree(big), 2, 8, 6))
cases.append(("root=%s p=2 q=4" % big, build_tree(big), 2, 4, 2))
cases.append(("root=[2,1] p=2 q=1", build_tree([2, 1]), 2, 1, 2))
cases.append(("root=[2,1] p=1 q=2", build_tree([2, 1]), 1, 2, 2))
cases.append(("root=[1,null,2] p=1 q=2", build_tree([1, None, 2]), 1, 2, 1))
cases.append(("root=%s p=3 q=5" % big, build_tree(big), 3, 5, 4))
cases.append(("root=%s p=0 q=5" % big, build_tree(big), 0, 5, 2))
cases.append(("root=%s p=7 q=9" % big, build_tree(big), 7, 9, 8))
cases.append(("root=%s p=9 q=3" % big, build_tree(big), 9, 3, 6))
neg = [0, -5, 5, -10, -2, 2, 10]
cases.append(("root=%s p=-10 q=-2" % neg, build_tree(neg), -10, -2, -5))
cases.append(("root=%s p=-2 q=2" % neg, build_tree(neg), -2, 2, 0))
ext = [10 ** 9, -10 ** 9]
cases.append(("root=[1e9,-1e9] p=1e9 q=-1e9", build_tree(ext), 10 ** 9, -10 ** 9, 10 ** 9))

# larger inputs for performance (iteratively built, shallow-ish skew)
bal = build_balanced(0, 99999)
cases.append(("balanced BST 0..99999 p=0 q=99999", bal, 0, 99999, ref_lca(bal, 0, 99999)))
cases.append(("balanced BST 0..99999 p=12345 q=12346", bal, 12345, 12346, ref_lca(bal, 12345, 12346)))
chain = build_chain(list(range(3000)), "right")
cases.append(("right chain 0..2999 p=100 q=2999", chain, 100, 2999, 100))

total = len(cases)
passed = 0
for i, (desc, root, pv, qv, exp) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        p = find_node(root, pv)
        q = find_node(root, qv)
        res = sol.lowestCommonAncestor(root, p, q)
        got = res.val if res is not None else None
        if got == exp:
            passed += 1
            print("PASS case %d" % i)
        else:
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (i, desc, exp, got))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (i, desc, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)