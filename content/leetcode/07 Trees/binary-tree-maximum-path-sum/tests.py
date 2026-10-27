import sys
import random
import threading
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


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def reference(root):
    """Independent iterative post-order reference."""
    best = root.val
    gain = {}
    stack = [(root, False)]
    while stack:
        node, seen = stack.pop()
        if node is None:
            continue
        if not seen:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
        else:
            l = max(gain.get(node.left, 0), 0)
            r = max(gain.get(node.right, 0), 0)
            best = max(best, node.val + l + r)
            gain[node] = node.val + max(l, r)
    return best


def chain(vals, side="left"):
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


def random_tree(n, seed, lo=-1000, hi=1000):
    rng = random.Random(seed)
    root = TreeNode(rng.randint(lo, hi))
    nodes = [root]
    while len(nodes) < n:
        parent = rng.choice(nodes)
        side = rng.choice(["left", "right"])
        if getattr(parent, side) is None:
            child = TreeNode(rng.randint(lo, hi))
            setattr(parent, side, child)
            nodes.append(child)
    return root


def describe(root):
    arr = tree_to_array(root)
    if len(arr) > 30:
        return f"<tree with {len(arr)} level-order entries>"
    return str(arr)


def make_cases():
    cases = []

    def add(builder, expected=None):
        cases.append((builder, expected))

    add(lambda: build_tree([1, 2, 3]), 6)
    add(lambda: build_tree([-10, 9, 20, None, None, 15, 7]), 42)
    add(lambda: build_tree([-3]), -3)
    add(lambda: build_tree([2, -1]), 2)
    add(lambda: build_tree([-2, -1]), -1)
    add(lambda: build_tree([1, -2, 3]), 4)
    add(lambda: build_tree([-1, -2, -3]), -1)
    add(lambda: build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]), 48)
    add(lambda: build_tree([-1, None, 9, -6, 3, None, None, None, -2]), 12)
    add(lambda: random_tree(300, seed=7), None)
    add(lambda: chain([1] * 30000, "left"), 30000)
    add(lambda: chain([-1000] * 30000, "right"), -1000)
    add(lambda: chain([1000 if i % 2 == 0 else -1 for i in range(30000)], "left"), None)
    add(lambda: random_tree(30000, seed=11), None)
    return cases


def run():
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
    exec(open("attempt.py").read(), ns)

    cases = make_cases()
    passed = 0
    for n, (builder, expected) in enumerate(cases, 1):
        root = None
        try:
            root = builder()
            if expected is None:
                expected = reference(root)
            got = ns["Solution"]().maxPathSum(root)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input={describe(root)}, expected={expected}, got={got}")
        except Exception as e:
            inp = describe(root) if root is not None else "<unbuilt>"
            print(f"FAIL case {n}: input={inp}, expected={expected}, got=error: {type(e).__name__}: {e}")

    print(f"{passed}/{len(cases)} passed")
    return passed == len(cases)


result = {}


def main():
    result["ok"] = run()


if __name__ == "__main__":
    sys.setrecursionlimit(200000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()
    if not result.get("ok"):
        sys.exit(1)
