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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_arr(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    """Build a tree from a LeetCode-style level-order list (None = missing)."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        node = q.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_arr(root):
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


def chain(n, side):
    root = TreeNode(1)
    cur = root
    for _ in range(n - 1):
        nxt = TreeNode(1)
        setattr(cur, side, nxt)
        cur = nxt
    return root


def zigzag(n):
    root = TreeNode(0)
    cur = root
    for i in range(n - 1):
        nxt = TreeNode(i % 100)
        if i % 2 == 0:
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


def perfect(depth):
    def make(d):
        if d == 0:
            return None
        return TreeNode(7, make(d - 1), make(d - 1))
    return make(depth)


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "deque": deque,
}
exec(open("attempt.py").read(), ns)


def run_solution(root):
    return ns["Solution"]().maxDepth(root)


# (description, builder returning root, expected)
CASES = [
    ("[3,9,20,null,null,15,7]", lambda: build_tree([3, 9, 20, None, None, 15, 7]), 3),
    ("[1,null,2]", lambda: build_tree([1, None, 2]), 2),
    ("[]", lambda: build_tree([]), 0),
    ("[0] (single node)", lambda: build_tree([0]), 1),
    ("[1,2] (left child only)", lambda: build_tree([1, 2]), 2),
    ("[1,2,3,4,5,6,7] (perfect, depth 3)", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), 3),
    ("[-100,-100,-100,-100] (negatives/duplicates)",
     lambda: build_tree([-100, -100, -100, -100]), 3),
    ("[1,2,3,4,null,null,5,6,null,null,7] (unbalanced)",
     lambda: build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7]), 4),
    ("[1,null,2,null,3,null,4,null,5] (right skew)",
     lambda: build_tree([1, None, 2, None, 3, None, 4, None, 5]), 5),
    ("left chain of 10000 nodes", lambda: chain(10000, "left"), 10000),
    ("right chain of 10000 nodes", lambda: chain(10000, "right"), 10000),
    ("zigzag chain of 5000 nodes", lambda: zigzag(5000), 5000),
    ("perfect tree depth 13 (8191 nodes)", lambda: perfect(13), 13),
]


def main():
    passed = 0
    total = len(CASES)
    for n, (desc, builder, expected) in enumerate(CASES, 1):
        try:
            root = builder()
            got = run_solution(root)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
        except BaseException as e:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got=exception {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    return passed == total


result = {"ok": False}


def target():
    result["ok"] = main()


if __name__ == "__main__":
    # Deep trees (10^4 nodes) need a high recursion limit and a large stack
    # so that recursive solutions are not penalised for Python's defaults.
    sys.setrecursionlimit(100000)
    try:
        threading.stack_size(256 * 1024 * 1024)
    except (ValueError, RuntimeError):
        pass
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if not result["ok"]:
        sys.exit(1)