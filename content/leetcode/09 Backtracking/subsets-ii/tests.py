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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
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


def canon(subsets):
    return sorted(tuple(sorted(s)) for s in subsets)


def reference(nums):
    from itertools import combinations
    seen = set()
    for r in range(len(nums) + 1):
        for c in combinations(sorted(nums), r):
            seen.add(c)
    return sorted(seen)


cases = [
    [1, 2, 2],
    [0],
    [1, 1],
    [2, 2, 2, 2],
    [-1, 0, 1],
    [-1, -1, 2, 2],
    [4, 4, 4, 1, 4],
    [3, 2, 1],
    [1, 2, 3, 4],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [-10, 10, -10, 10, 0],
    [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
]

passed = 0
total = len(cases)
for idx, nums in enumerate(cases, 1):
    expected = reference(nums)
    original = list(nums)
    try:
        sol = ns["Solution"]()
        got = sol.subsetsWithDup(list(nums))
        got_c = canon(got)
        if got_c == expected and len(got) == len(expected):
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={original}, expected={expected}, got={got_c}")
    except Exception as e:
        print(f"FAIL case {idx}: input={original}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
