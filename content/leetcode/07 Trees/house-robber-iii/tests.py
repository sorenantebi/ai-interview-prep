import sys
from typing import List, Optional, Dict
from collections import deque

sys.setrecursionlimit(50000)


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


def build_chain(n, val=1):
    root = TreeNode(val)
    cur = root
    for _ in range(n - 1):
        cur.left = TreeNode(val)
        cur = cur.left
    return root


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ("[3,2,3,null,3,null,1]", lambda: build_tree([3, 2, 3, None, 3, None, 1]), 7),
    ("[3,4,5,1,3,null,1]", lambda: build_tree([3, 4, 5, 1, 3, None, 1]), 9),
    ("[5]", lambda: build_tree([5]), 5),
    ("[0]", lambda: build_tree([0]), 0),
    ("[1,2]", lambda: build_tree([1, 2]), 2),
    ("[2,1,3,null,4]", lambda: build_tree([2, 1, 3, None, 4]), 7),
    ("[4,1,null,2,null,3]", lambda: build_tree([4, 1, None, 2, None, 3]), 7),
    ("[1]*7 (perfect tree)", lambda: build_tree([1] * 7), 5),
    ("[10,1,1,10,null,null,10]", lambda: build_tree([10, 1, 1, 10, None, None, 10]), 30),
    ("[10000,10000,10000]", lambda: build_tree([10000, 10000, 10000]), 20000),
    ("left chain of 5000 nodes, all 1", lambda: build_chain(5000), 2500),
    ("perfect tree of 8191 nodes, all 1", lambda: build_tree([1] * 8191), 5461),
]

passed = 0
total = len(cases)
for idx, (label, builder, expected) in enumerate(cases, 1):
    try:
        root = builder()
        got = ns["Solution"]().rob(root)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={label}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={label}, expected={expected}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
