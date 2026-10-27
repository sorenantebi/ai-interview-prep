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


def brute(height):
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, min(height[i], height[j]) * (j - i))
    return best


def make_large_random():
    import random
    rnd = random.Random(12345)
    return [rnd.randint(0, 10000) for _ in range(100000)]


def reference(height):
    l, r = 0, len(height) - 1
    res = 0
    while l < r:
        res = max(res, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return res


large_random = make_large_random()
large_asc = list(range(10000)) * 10
large_same = [10000] * 100000

cases = [
    ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
    ([1, 1], 1),
    ([0, 0], 0),
    ([0, 5], 0),
    ([5, 0, 0, 0, 5], 20),
    ([4, 3, 2, 1, 4], 16),
    ([1, 2, 1], 2),
    ([2, 3, 4, 5, 18, 17, 6], 17),
    ([10000, 10000], 10000),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], brute([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
    ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], brute([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])),
    (large_same, 10000 * 99999),
    (large_random, reference(large_random)),
    (large_asc, reference(large_asc)),
]


def run():
    passed = 0
    total = len(cases)
    for n, (height, expected) in enumerate(cases, 1):
        shown = height if len(height) <= 20 else f"<list of length {len(height)}>"
        try:
            got = ns["Solution"]().maxArea(list(height))
            if got == expected:
                passed += 1
                print(f"PASS case {n}")
            else:
                print(f"FAIL case {n}: input={shown}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input={shown}, expected={expected}, got=error: {type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


run()