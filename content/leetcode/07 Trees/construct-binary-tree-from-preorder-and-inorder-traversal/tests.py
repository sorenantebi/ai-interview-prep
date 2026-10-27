import sys
import random
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


def build_tree(values):
    """Level-order list (None for missing) -> tree."""
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


def serialize(root):
    """Tree -> level-order list with trailing Nones stripped (canonical form)."""
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


def canon(values):
    values = list(values)
    while values and values[-1] is None:
        values.pop()
    return values


def preorder_of(root):
    res, stack = [], [root]
    while stack:
        n = stack.pop()
        if n is None:
            continue
        res.append(n.val)
        stack.append(n.right)
        stack.append(n.left)
    return res


def inorder_of(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res


def random_tree(n, seed):
    rnd = random.Random(seed)
    vals = list(range(-1500, -1500 + n))
    rnd.shuffle(vals)
    root = TreeNode(vals[0])
    slots = [(root, "left"), (root, "right")]
    for v in vals[1:]:
        idx = rnd.randrange(len(slots))
        slots[idx], slots[-1] = slots[-1], slots[idx]
        parent, side = slots.pop()
        node = TreeNode(v)
        setattr(parent, side, node)
        slots.append((node, "left"))
        slots.append((node, "right"))
    return root


def chain(n, side):
    root = TreeNode(0)
    cur = root
    for v in range(1, n):
        nxt = TreeNode(v)
        setattr(cur, side, nxt)
        cur = nxt
    return root


def case_from_tree(root):
    return (preorder_of(root), inorder_of(root), serialize(root))


big_random = random_tree(3000, 12345)
big_left = chain(3000, "left")
big_right = chain(3000, "right")
mid_random = random_tree(500, 777)

cases = [
    # examples
    ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
    ([-1], [-1], [-1]),
    # two nodes, left child
    ([1, 2], [2, 1], [1, 2]),
    # two nodes, right child
    ([1, 2], [1, 2], [1, None, 2]),
    # left-skewed
    ([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], [1, 2, None, 3, None, 4, None, 5, None, 6]),
    # right-skewed
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, None, 2, None, 3, None, 4, None, 5]),
    # perfect tree
    ([1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7], [1, 2, 3, 4, 5, 6, 7]),
    # negatives
    ([0, -5, -10, -3, 4], [-10, -5, -3, 0, 4], [0, -5, 4, -10, -3]),
    # zigzag
    ([1, 2, 3, 4], [2, 4, 3, 1], [1, 2, None, None, 3, 4]),
    # medium random
    case_from_tree(mid_random),
    # large random (3000)
    case_from_tree(big_random),
    # large left chain
    case_from_tree(big_left),
    # large right chain
    case_from_tree(big_right),
]

ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def fmt(lst):
    if len(lst) > 20:
        return "<len %d>" % len(lst)
    return str(lst)


passed = 0
total = len(cases)
for i, (pre, ino, expected) in enumerate(cases, 1):
    desc = "preorder=%s, inorder=%s" % (fmt(pre), fmt(ino))
    try:
        got_root = ns["Solution"]().buildTree(list(pre), list(ino))
        got = canon(serialize(got_root))
        exp = canon(expected)
        if got == exp:
            print("PASS case %d" % i)
            passed += 1
        else:
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (i, desc, fmt(exp), fmt(got)))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (i, desc, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
