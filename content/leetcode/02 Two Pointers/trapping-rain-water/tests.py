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


def brute(height):
    n = len(height)
    total = 0
    lm = 0
    left = []
    for h in height:
        lm = max(lm, h)
        left.append(lm)
    rm = 0
    right = [0] * n
    for i in range(n - 1, -1, -1):
        rm = max(rm, height[i])
        right[i] = rm
    for i in range(n):
        total += min(left[i], right[i]) - height[i]
    return total


def run(height):
    return ns["Solution"]().trap(list(height))


big_mountain = list(range(0, 10001)) + list(range(10000, -1, -1))
big_valley = list(range(10000, -1, -1)) + list(range(0, 10001))
big_flat = [100000] * 20000
big_zigzag = [100000 if i % 2 == 0 else 0 for i in range(20000)]

cases = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([5], 0),
    ([3, 3], 0),
    ([0, 0, 0, 0], 0),
    ([1, 2, 3, 4, 5], 0),
    ([5, 4, 3, 2, 1], 0),
    ([5, 0, 5], 5),
    ([3, 0, 0, 2, 0, 4], 10),
    ([2, 0, 2, 0, 2], 4),
    (big_mountain, 0),
    (big_valley, brute(big_valley)),
    (big_flat, 0),
    (big_zigzag, brute(big_zigzag)),
]

passed = 0
total = len(cases)
for idx, (height, expected) in enumerate(cases, 1):
    shown = height if len(height) <= 20 else f"<list of length {len(height)}>"
    try:
        got = run(height)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={shown}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={shown}, expected={expected}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
