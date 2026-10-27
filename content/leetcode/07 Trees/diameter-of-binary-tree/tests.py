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


def build_tree(values):
    """Build a tree from a LeetCode-style level-order list (None = missing)."""
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


def tree_to_list(root):
    """Serialize a tree to a LeetCode-style level-order list."""
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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def chain(n, direction="left"):
    """Chain of n nodes, all going left, right, or alternating."""
    if n == 0:
        return None
    root = TreeNode(1)
    cur = root
    for k in range(1, n):
        d = direction if direction != "zigzag" else ("left" if k % 2 else "right")
        nxt = TreeNode(1)
        if d == "left":
            cur.left = nxt
        else:
            cur.right = nxt
        cur = nxt
    return root


def heap_tree(n):
    nodes = [TreeNode(i % 201 - 100) for i in range(n)]
    for i in range(n):
        if 2 * i + 1 < n:
            nodes[i].left = nodes[2 * i + 1]
        if 2 * i + 2 < n:
            nodes[i].right = nodes[2 * i + 2]
    return nodes[0]


def two_chains(k):
    root = TreeNode(1)
    root.left = chain(k, "left")
    root.right = chain(k, "right")
    return root


def ref_diameter(root):
    """Iterative reference used only to compute expected values for big trees."""
    best = 0
    heights = {}
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if node is None:
            continue
        if done:
            l = heights.get(id(node.left), 0)
            r = heights.get(id(node.right), 0)
            best = max(best, l + r)
            heights[id(node)] = 1 + max(l, r)
        else:
            stack.append((node, True))
            stack.append((node.left, False))
            stack.append((node.right, False))
    return best


def make_cases():
    big_heap = heap_tree(10000)
    return [
        # (description, tree factory, expected)
        ("[1,2,3,4,5]", lambda: build_tree([1, 2, 3, 4, 5]), 3),
        ("[1,2]", lambda: build_tree([1, 2]), 1),
        ("[1]", lambda: build_tree([1]), 0),
        ("[1,None,2]", lambda: build_tree([1, None, 2]), 1),
        ("[1,2,None,3,None,4]", lambda: build_tree([1, 2, None, 3, None, 4]), 3),
        ("[1,2,None,3,4,5,None,None,6] (path avoids root)",
         lambda: build_tree([1, 2, None, 3, 4, 5, None, None, 6]), 4),
        ("[-1,-2,-3]", lambda: build_tree([-1, -2, -3]), 2),
        ("[1..7] perfect tree", lambda: build_tree([1, 2, 3, 4, 5, 6, 7]), 4),
        ("two chains of 3 under root", lambda: two_chains(3), 6),
        ("left-skewed 10000 nodes", lambda: chain(10000, "left"), 9999),
        ("zigzag 10000 nodes", lambda: chain(10000, "zigzag"), 9999),
        ("complete tree 10000 nodes", lambda: heap_tree(10000), ref_diameter(big_heap)),
    ]


def run():
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List,
          "Optional": Optional, "Dict": Dict}
    exec(open("attempt.py").read(), ns)

    cases = make_cases()
    passed = 0
    for n, (desc, factory, expected) in enumerate(cases, 1):
        try:
            root = factory()
            got = ns["Solution"]().diameterOfBinaryTree(root)
            if got == expected:
                passed += 1
                print(f"PASS case {n}")
            else:
                print(f"FAIL case {n}: input={desc}, expected={expected}, got={got}")
        except BaseException as e:
            print(f"FAIL case {n}: input={desc}, expected={expected}, got=error {type(e).__name__}: {e}")

    print(f"{passed}/{len(cases)} passed")
    return passed == len(cases)


result = {}


def main():
    result["ok"] = run()


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    threading.stack_size(256 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()
    if not result.get("ok"):
        sys.exit(1)