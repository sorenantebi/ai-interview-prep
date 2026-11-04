import sys
import random
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

rng = random.Random(12345)
large_random = [rng.randint(-50000, 50000) for _ in range(50000)]
large_dups = [rng.randint(-5, 5) for _ in range(50000)]
large_ascending = list(range(-25000, 25000))
large_descending = list(range(25000, -25000, -1))

# (input, expected)
cases = [
    ([5, 2, 3, 1], [1, 2, 3, 5]),
    ([5, 1, 1, 2, 0, 0], [0, 0, 1, 1, 2, 5]),
    ([7], [7]),
    ([2, 1], [1, 2]),
    ([3, 3, 3, 3], [3, 3, 3, 3]),
    ([-1, -5, -3, -2, -4], [-5, -4, -3, -2, -1]),
    ([-50000, 50000, 0, -1, 1], [-50000, -1, 0, 1, 50000]),
    ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]),
    ([0, -1, 0, -1, 2, 2, -2], [-2, -1, -1, 0, 0, 2, 2]),
    (large_random, sorted(large_random)),
    (large_dups, sorted(large_dups)),
    (large_ascending, large_ascending[:]),
    (large_descending, sorted(large_descending)),
]


def short(x):
    s = repr(x)
    return s if len(s) <= 80 else s[:77] + "..."


passed = 0
total = len(cases)
for idx, (inp, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        arg = list(inp)
        got = sol.sortArray(arg)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={short(inp)}, expected={short(expected)}, got={short(got)}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)