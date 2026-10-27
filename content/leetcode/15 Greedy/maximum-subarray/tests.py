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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
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


def brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s > best:
                best = s
    return best


# Deterministic pseudo-random array checked against brute force
_seed = 12345
_rand = []
for _ in range(300):
    _seed = (_seed * 1103515245 + 12345) % (2 ** 31)
    _rand.append(_seed % 20001 - 10000)

cases = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
    ([1], 1),
    ([5, 4, -1, 7, 8], 23),
    ([-1], -1),
    ([-3, -2, -5, -1, -4], -1),
    ([0, 0, 0], 0),
    ([-1, 0, -2], 0),
    ([2, -1], 2),
    ([-1, 2], 2),
    ([8, -19, 5, -4, 20], 21),
    (_rand, brute(_rand)),
    ([10000] * 100000, 10000 * 100000),
    ([10000, -10000] * 50000, 10000),
    ([-1] * 100000, -1),
    ([-10000] * 50000 + [10000] * 50000, 10000 * 50000),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
for n, (nums, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().maxSubArray(list(nums))
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(nums)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(nums)}, expected={expected}, got=exception: {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)