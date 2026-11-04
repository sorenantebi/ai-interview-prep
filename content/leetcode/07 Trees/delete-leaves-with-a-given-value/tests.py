import sys
from typing import List, Optional, Dict
from collections import deque

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


def serialize_tree(root):
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


def short(x, limit=60):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(len=%d)" % len(x)


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

# large inputs
chain_all = [1] * 3000                       # left-skewed chain, built level-order: 1,1,null,1,null,...
chain_vals = []
for i in range(3000):
    chain_vals.append(1)
    if i < 2999:
        chain_vals.append(None)
# right-skewed chain: node, null, next ... would be left-skewed if we place next as left child
left_chain = []
for i in range(3000):
    left_chain.append(1)
    if i < 2999:
        pass
# build left chain directly: each node's left is the next, right None
left_chain_level = []
for i in range(3000):
    left_chain_level.append(1 if i < 2999 else 2)
    if i < 2999:
        left_chain_level.append(None)
left_chain_level_all_ones = [1 if True else 0] * 0
for i in range(3000):
    left_chain_level_all_ones.append(1)
    if i < 2999:
        left_chain_level_all_ones.append(None)

# expected for chain with leaf 2 removed (target 2): 2999 ones as a left chain
expected_chain_2999 = []
for i in range(2999):
    expected_chain_2999.append(1)
    if i < 2998:
        expected_chain_2999.append(None)

# (tree level-order list, target, expected level-order list)
cases = [
    ([1, 2, 3, 2, None, 2, 4], 2, [1, None, 3, None, 4]),
    ([1, 3, 3, 3, 2], 3, [1, 3, None, None, 2]),
    ([1, 2, None, 2, None, 2], 2, [1]),
    ([1], 1, []),
    ([1], 2, [1]),
    ([2, 2, 2], 2, []),
    ([1, 1, 1], 1, []),
    ([1, 2, 3], 5, [1, 2, 3]),
    ([1, 2, 3], 2, [1, None, 3]),
    ([2, 1, 2, None, None, 2, 1], 2, [2, 1, 2, None, None, None, 1]),
    ([1, 2, 3, 4, 5, 6, 7], 4, [1, 2, 3, None, 5, 6, 7]),
    (left_chain_level_all_ones, 1, []),
    (left_chain_level, 2, expected_chain_2999),
]

passed = 0
total = len(cases)
for n, (vals, target, expected) in enumerate(cases, 1):
    try:
        root = build_tree(vals)
        res = ns["Solution"]().removeLeafNodes(root, target)
        got = serialize_tree(res)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input={short(vals)}, target={target}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(vals)}, target={target}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)