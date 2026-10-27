import sys
from typing import List, Optional, Dict
from itertools import combinations


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


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
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


def expected_subsets(nums):
    res = []
    for k in range(len(nums) + 1):
        for c in combinations(nums, k):
            res.append(list(c))
    return res


cases = [
    [1, 2, 3],
    [0],
    [5],
    [-1],
    [1, 2],
    [3, 1, 2],
    [-10, 10],
    [-3, -2, -1, 0, 1],
    [10, -10, 0, 7],
    list(range(1, 7)),
    list(range(-5, 5)),
    list(range(-5, 5)) + [10],  # length 11 is beyond constraints; replaced below
]
# keep within constraints: max length 10
cases[-1] = [-10, -7, -4, -1, 2, 5, 8, 10, 3, 0]


def run():
    passed = 0
    total = len(cases)
    for idx, nums in enumerate(cases, 1):
        inp = list(nums)
        exp = canon(expected_subsets(nums))
        try:
            got_raw = ns["Solution"]().subsets(list(nums))
            got = canon(got_raw)
            ok = got == exp and len(got_raw) == len(exp)
        except Exception as e:
            print(f"FAIL case {idx}: input={inp}, error={type(e).__name__}: {e}")
            continue
        if ok:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={inp}, expected={exp}, got={got_raw}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()