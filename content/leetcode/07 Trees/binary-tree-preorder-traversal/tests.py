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


def build_tree(vals):
    """Build a tree from a LeetCode-style level-order list (None = missing)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    qi = 0
    while qi < len(queue) and i < len(vals):
        node = queue[qi]
        qi += 1
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    """Serialize a tree to a LeetCode-style level-order list."""
    if root is None:
        return []
    out = []
    queue = [root]
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def build_list(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_py(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def make_left_chain(vals):
    root = None
    for v in reversed(vals):
        root = TreeNode(v, root, None)
    return root


def make_right_chain(vals):
    root = None
    for v in reversed(vals):
        root = TreeNode(v, None, root)
    return root


big_vals = [(i * 7) % 201 - 100 for i in range(100)]

# (description, tree builder, expected)
cases = [
    ("[1,null,2,3]", lambda: build_tree([1, None, 2, 3]), [1, 2, 3]),
    ("[1,2,3,4,5,null,8,null,null,6,7,9]",
     lambda: build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9]),
     [1, 2, 4, 5, 6, 7, 3, 8, 9]),
    ("[]", lambda: build_tree([]), []),
    ("[1]", lambda: build_tree([1]), [1]),
    ("left skewed [1,2,null,3,null,4]", lambda: build_tree([1, 2, None, 3, None, 4]), [1, 2, 3, 4]),
    ("right skewed [1,null,2,null,3,null,4]", lambda: build_tree([1, None, 2, None, 3, None, 4]), [1, 2, 3, 4]),
    ("duplicates [-1,-1,-1]", lambda: build_tree([-1, -1, -1]), [-1, -1, -1]),
    ("negatives/bounds [0,-100,100,-100,null,null,100]",
     lambda: build_tree([0, -100, 100, -100, None, None, 100]),
     [0, -100, -100, 100, 100]),
    ("complete [1,2,3,4,5,6,7]", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), [1, 2, 4, 5, 3, 6, 7]),
    ("zigzag [5,3,null,null,4,2]", lambda: build_tree([5, 3, None, None, 4, 2]), [5, 3, 4, 2]),
    ("large left chain of 100 nodes", lambda: make_left_chain(big_vals), list(big_vals)),
    ("large right chain of 100 nodes", lambda: make_right_chain(big_vals), list(big_vals)),
]

passed = 0
total = len(cases)
for n, (desc, builder, expected) in enumerate(cases, 1):
    try:
        root = builder()
        got = ns["Solution"]().preorderTraversal(root)
        if list(got) == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={desc}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)