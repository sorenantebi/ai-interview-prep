import sys
import heapq
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


def serialize_list(head):
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


def serialize_tree(root):
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict, "heapq": heapq}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


def reference(stones):
    s = sorted(stones)
    while len(s) > 1:
        y = s.pop()
        x = s.pop()
        if y != x:
            s.append(y - x)
            s.sort()
    return s[0] if s else 0


rng = random.Random(42)
rand_a = [rng.randint(1, 1000) for _ in range(30)]
rand_b = [rng.randint(1, 10) for _ in range(30)]

cases = [
    ([2, 7, 4, 1, 8, 1], 1),
    ([1], 1),
    ([3, 3], 0),
    ([1, 3], 2),
    ([10, 4, 2, 10], 2),
    ([5, 5, 5], 5),
    ([1, 1, 1, 1, 1], 1),
    ([9, 3, 2, 10], 0),
    ([31, 26, 33, 21, 40], 9),
    ([2, 2, 3], 1),
    ([1, 2, 3, 6], 0),
    ([1000] * 30, 0),
    ([1000, 1], 999),
    (list(range(1, 31)), reference(list(range(1, 31)))),
    (rand_a, reference(rand_a)),
    (rand_b, reference(rand_b)),
]

passed = 0
for i, (stones, expected) in enumerate(cases, 1):
    try:
        got = Solution().lastStoneWeight(list(stones))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={stones}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={stones}, expected={expected}, got={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)