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


def brute(a, b):
    m = sorted(a + b)
    n = len(m)
    if n % 2:
        return float(m[n // 2])
    return (m[n // 2 - 1] + m[n // 2]) / 2


rng = random.Random(12345)


def rand_sorted(size, lo=-10**6, hi=10**6):
    return sorted(rng.randint(lo, hi) for _ in range(size))


big1 = rand_sorted(1000)
big2 = rand_sorted(1000)
dup1 = rand_sorted(500, -5, 5)
dup2 = rand_sorted(700, -5, 5)

cases = [
    ([1, 3], [2], 2.0),
    ([1, 2], [3, 4], 2.5),
    ([], [1], 1.0),
    ([2], [], 2.0),
    ([1], [2], 1.5),
    ([], [1, 2, 3, 4], 2.5),
    ([5, 6, 7], [1, 2, 3], 4.0),
    ([-5, -3, -1], [-4, -2], -3.0),
    ([2, 2, 2], [2, 2], 2.0),
    ([1, 2, 3, 4, 5], [100, 200, 300], 4.5),
    ([-1000000], [1000000], 0.0),
    ([0, 0], [0, 0], 0.0),
    (dup1, dup2, brute(dup1, dup2)),
    (big1, big2, brute(big1, big2)),
    (big1, [], brute(big1, [])),
]

passed = 0
total = len(cases)
for idx, (a, b, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.findMedianSortedArrays(list(a), list(b))
        if abs(float(got) - expected) < 1e-5:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input={a if len(a) < 20 else '<len %d>' % len(a)}, "
                  f"{b if len(b) < 20 else '<len %d>' % len(b)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={a if len(a) < 20 else '<len %d>' % len(a)}, "
              f"{b if len(b) < 20 else '<len %d>' % len(b)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)