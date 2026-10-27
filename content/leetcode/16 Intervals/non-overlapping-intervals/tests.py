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
    q = [root]
    i = 1
    while q and i < len(vals):
        node = q.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    out = []
    q = [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def ref(intervals):
    """Independent reference: max chain via DP, answer = n - chain."""
    iv = sorted(intervals, key=lambda x: (x[1], x[0]))
    n = len(iv)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return n - max(dp)


rng = random.Random(12345)
random_small = []
for _ in range(3):
    n = rng.randint(5, 12)
    cur = []
    for _ in range(n):
        s = rng.randint(-10, 10)
        e = rng.randint(s + 1, s + 8)
        cur.append([s, e])
    random_small.append(cur)

cases = [
    ([[1, 2], [2, 3], [3, 4], [1, 3]], 1),
    ([[1, 2], [1, 2], [1, 2]], 2),
    ([[1, 2], [2, 3]], 0),
    ([[0, 1]], 0),
    ([[-50000, 50000], [-1, 0], [0, 1]], 1),
    ([[1, 100], [11, 22], [1, 11], [2, 12]], 2),
    ([[-3, -2], [-2, -1], [-3, -1], [-5, -4]], 1),
    ([[1, 5], [2, 3], [3, 4], [4, 5]], 1),
    ([[1, 2], [3, 4], [5, 6]], 0),
    ([[i, i + 1] for i in range(-50000, 50000)], 0),
    ([[1, 2]] * 100000, 99999),
    ([[-50000, 50000 - i] for i in range(100000)], 99999),
]
for iv in random_small:
    cases.append((iv, ref(iv)))

passed = 0
total = len(cases)
for idx, (iv, expected) in enumerate(cases, 1):
    label = iv if len(iv) <= 20 else f"<{len(iv)} intervals>"
    try:
        arg = [list(x) for x in iv]
        got = ns["Solution"]().eraseOverlapIntervals(arg)
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={label}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={label}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)