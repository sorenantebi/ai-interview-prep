import sys
import threading
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


def build_chain(vals, side):
    """Build a degenerate tree iteratively (left or right chain)."""
    root = TreeNode(vals[0])
    cur = root
    for v in vals[1:]:
        nxt = TreeNode(v)
        if side == "left":
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


N = 100000

# (description, tree factory, expected)
CASES = [
    ("[3,1,4,3,null,1,5]", lambda: build_tree([3, 1, 4, 3, None, 1, 5]), 4),
    ("[3,3,null,4,2]", lambda: build_tree([3, 3, None, 4, 2]), 3),
    ("[1]", lambda: build_tree([1]), 1),
    ("decreasing [5,4,3,2,1]", lambda: build_tree([5, 4, 3, 2, 1]), 1),
    ("increasing perfect [1..7]", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), 7),
    ("all negative [-1,-2,-3]", lambda: build_tree([-1, -2, -3]), 1),
    ("duplicates [2,2,2,2,2]", lambda: build_tree([2, 2, 2, 2, 2]), 5),
    ("single min value [-10000]", lambda: build_tree([-10000]), 1),
    ("extremes [10000,-10000,10000]", lambda: build_tree([10000, -10000, 10000]), 2),
    (
        "mixed negatives/positives [-5,-10,0,null,-3,-1,7]",
        lambda: build_tree([-5, -10, 0, None, -3, -1, 7]),
        4,
    ),
    (
        "right skew [1,null,2,null,3,null,2]",
        lambda: build_tree([1, None, 2, None, 3, None, 2]),
        3,
    ),
    (
        "long decreasing left chain 100000",
        lambda: build_chain([10000 - min(i, 20000) for i in range(N)], "left"),
        1,
    ),
    (
        "long increasing right chain 100000",
        lambda: build_chain([-10000 + min(i, 20000) for i in range(N)], "right"),
        N,
    ),
    (
        "long equal-valued chain 100000",
        lambda: build_chain([5] * N, "left"),
        N,
    ),
]


def run():
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
    exec(open("attempt.py").read(), ns)

    passed = 0
    total = len(CASES)
    for n, (desc, factory, expected) in enumerate(CASES, 1):
        try:
            root = factory()
            got = ns["Solution"]().goodNodes(root)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
        except BaseException as e:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got=exception {type(e).__name__}: {e}")

    print(f"{passed}/{total} passed")
    return passed == total


def main():
    result = {}

    def target():
        result["ok"] = run()

    # deep chains: allow recursive solutions to work
    sys.setrecursionlimit(1000000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()