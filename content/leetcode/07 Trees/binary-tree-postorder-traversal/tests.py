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


def tree_to_array(root):
    if not root:
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

N = None

left_chain = [1]
for _ in range(99):
    left_chain += [N]
left_chain_vals = None


def chain_tree(n, side):
    root = TreeNode(1)
    cur = root
    for v in range(2, n + 1):
        nxt = TreeNode(v)
        if side == "left":
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


# (description, tree builder, expected)
cases = [
    ("[1,null,2,3]", lambda: build_tree([1, N, 2, 3]), [3, 2, 1]),
    ("[1,2,3,4,5,null,8,null,null,6,7,9]",
     lambda: build_tree([1, 2, 3, 4, 5, N, 8, N, N, 6, 7, 9]),
     [4, 6, 7, 5, 2, 9, 8, 3, 1]),
    ("[]", lambda: build_tree([]), []),
    ("[1]", lambda: build_tree([1]), [1]),
    ("[1,2,null,3,null,4] (left chain)", lambda: build_tree([1, 2, N, 3, N, 4]), [4, 3, 2, 1]),
    ("[5,null,6,null,7] (right chain)", lambda: build_tree([5, N, 6, N, 7]), [7, 6, 5]),
    ("[0,-1,1,-2,null,null,-3] (negatives)",
     lambda: build_tree([0, -1, 1, -2, N, N, -3]),
     [-2, -1, -3, 1, 0]),
    ("[1,2,3,4,5,6,7] (perfect)", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), [4, 5, 2, 6, 7, 3, 1]),
    ("[7,7,7] (duplicates)", lambda: build_tree([7, 7, 7]), [7, 7, 7]),
    ("[1,2,3,null,4] (mixed)", lambda: build_tree([1, 2, 3, N, 4]), [4, 2, 3, 1]),
    ("[10,20,null,null,30,40] (zigzag)", lambda: build_tree([10, 20, N, N, 30, 40]), [40, 30, 20, 10]),
    ("left chain of 100 nodes", lambda: chain_tree(100, "left"), list(range(100, 0, -1))),
    ("right chain of 100 nodes", lambda: chain_tree(100, "right"), list(range(100, 0, -1))),
]

passed = 0
total = len(cases)
for idx, (desc, make, expected) in enumerate(cases, 1):
    shown = desc if len(desc) < 80 else desc[:77] + "..."
    try:
        root = make()
        got = ns["Solution"]().postorderTraversal(root)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            exp_s = str(expected) if len(str(expected)) < 100 else str(expected)[:97] + "..."
            got_s = str(got) if len(str(got)) < 100 else str(got)[:97] + "..."
            print(f"FAIL case {idx}: input={shown}, expected={exp_s}, got={got_s}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)