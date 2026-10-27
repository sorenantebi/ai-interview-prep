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
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def brute(nums, target):
    sums = {0: 1}
    for x in nums:
        new = {}
        for s, c in sums.items():
            new[s + x] = new.get(s + x, 0) + c
            new[s - x] = new.get(s - x, 0) + c
        sums = new
    return sums.get(target, 0)


cases = [
    ([1, 1, 1, 1, 1], 3, 5),
    ([1], 1, 1),
    ([0, 0], 0, 4),
    ([1], -1, 1),
    ([1], 2, 0),
    ([1, 2], 0, 0),
    ([0], 0, 2),
    ([1, 2, 3], 6, 1),
    ([1, 2, 3], -6, 1),
    ([1, 2, 1], 0, 2),
    ([0] * 20, 0, 2 ** 20),
    ([1000], 1000, 1),
    ([1] * 20, 0, brute([1] * 20, 0)),
    (list(range(1, 15)) + [0] * 6, 5, brute(list(range(1, 15)) + [0] * 6, 5)),
    ([7, 9, 3, 8, 0, 2, 4, 8, 3, 9, 0, 1, 5, 6, 2, 4, 3, 7, 1, 2], 11,
     brute([7, 9, 3, 8, 0, 2, 4, 8, 3, 9, 0, 1, 5, 6, 2, 4, 3, 7, 1, 2], 11)),
]

passed = 0
total = len(cases)
for n, (nums, target, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().findTargetSumWays(list(nums), target)
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input=nums={nums}, target={target}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=nums={nums}, target={target}, expected={expected}, got=exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
