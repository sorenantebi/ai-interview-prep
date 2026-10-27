import sys
from collections import deque
from typing import List, Optional, Dict

sys.setrecursionlimit(200000)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def chain(values, direction):
    """Build a degenerate tree, each node the child of the previous one."""
    root = TreeNode(values[0])
    cur = root
    for v in values[1:]:
        node = TreeNode(v)
        if direction == "right":
            cur.right = node
        else:
            cur.left = node
        cur = node
    return root


def describe(root):
    arr = tree_to_array(root)
    if len(arr) > 30:
        return f"<tree with {len(arr)} entries>"
    return str(arr)


MIN_INT = -2**31
MAX_INT = 2**31 - 1

N = 10000

cases = [
    # (tree, expected)
    (build_tree([2, 1, 3]), True),
    (build_tree([5, 1, 4, None, None, 3, 6]), False),
    (build_tree([5, 4, 6, None, None, 3, 7]), False),
    (build_tree([1]), True),
    (build_tree([1, 1]), False),
    (build_tree([1, None, 1]), False),
    (build_tree([2, 2, 2]), False),
    (build_tree([MIN_INT]), True),
    (build_tree([MIN_INT, None, MAX_INT]), True),
    (build_tree([MAX_INT, MIN_INT, None]), True),
    (build_tree([10, 5, 15, None, None, 6, 20]), False),
    (build_tree([3, 1, 5, 0, 2, 4, 6]), True),
    (build_tree([-3, -5, -1, -6, -4, -2, 0]), True),
    (build_tree([5, 3, 8, 1, 4, 7, 9, None, None, None, 5]), False),
    (chain(list(range(N)), "right"), True),
    (chain(list(range(N, 0, -1)), "left"), True),
    (chain(list(range(N - 1)) + [0], "right"), False),
]

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

passed = 0
total = len(cases)

for idx, (tree, expected) in enumerate(cases, 1):
    desc = describe(tree)
    try:
        got = ns["Solution"]().isValidBST(tree)
        if isinstance(got, bool) and got == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            print(f"FAIL case {idx}: input={desc}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={desc}, expected={expected}, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)