import sys
import random
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


def build_list(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_arr(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_arr(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def make_wide():
    rnd = random.Random(12345)
    n = 2000
    edges = set()
    while len(edges) < 5000:
        a = rnd.randrange(1, n)
        b = rnd.randrange(0, a)
        edges.add((a, b))
    return n, [list(e) for e in sorted(edges)]


wide_n, wide_edges = make_wide()
chain = [[i, i - 1] for i in range(1, 2000)]

cases = [
    ((2, [[1, 0]]), True),
    ((2, [[1, 0], [0, 1]]), False),
    ((1, []), True),
    ((1, [[0, 0]]), False),
    ((3, []), True),
    ((3, [[1, 0], [2, 1], [0, 2]]), False),
    ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), True),
    ((5, [[1, 0], [2, 3], [3, 4], [4, 2]]), False),
    ((4, [[1, 0], [3, 2]]), True),
    ((4, [[1, 0], [2, 1], [3, 2], [1, 3]]), False),
    ((2000, chain), True),
    ((2000, chain + [[0, 1999]]), False),
    ((wide_n, wide_edges), True),
]


def describe(args):
    n, prereq = args
    if len(prereq) > 20:
        return f"({n}, <{len(prereq)} pairs>)"
    return f"({n}, {prereq})"


passed = 0
for i, (args, expected) in enumerate(cases, 1):
    try:
        got = Solution().canFinish(args[0], [list(p) for p in args[1]])
        ok = got == expected
    except Exception as e:
        got = f"exception: {type(e).__name__}: {e}"
        ok = False
    if ok:
        passed += 1
        print(f"PASS case {i}")
    else:
        print(f"FAIL case {i}: input={describe(args)}, expected={expected}, got={got}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)