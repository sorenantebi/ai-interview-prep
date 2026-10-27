import sys
import heapq
import bisect
import random
import time
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
    out, queue = [], [root]
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


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict, "heapq": heapq}
exec(open("attempt.py").read(), ns)
KthLargest = ns["KthLargest"]


def brute(k, nums, adds):
    data = sorted(nums)
    res = [None]
    for v in adds:
        bisect.insort(data, v)
        res.append(data[-k])
    return res


def run(k, nums, adds):
    obj = KthLargest(k, list(nums))
    res = [None]
    for v in adds:
        res.append(obj.add(v))
    return res


random.seed(12345)
big_nums = [random.randint(-10**4, 10**4) for _ in range(10**4)]
big_adds = [random.randint(-10**4, 10**4) for _ in range(10**4)]

# (k, nums, adds, expected or None to compute by brute force, time_limit or None)
cases = [
    (3, [4, 5, 8, 2], [3, 5, 10, 9, 4], [None, 4, 5, 5, 8, 8], None),
    (1, [], [-3, -2, -4], [None, -3, -2, -2], None),
    (1, [5], [1], [None, 5], None),
    (2, [1], [0], [None, 0], None),
    (2, [], [7, 7], [None, None, 7][:1] + [None] if False else None, None),
    (3, [5, 5, 5], [5, 5], [None, 5, 5], None),
    (2, [-10, -20, -5], [-30, -1, -7, -6], None, None),
    (4, [1, 2, 3], [4, 0, 10, -1, 3], None, None),
    (1, [10000, -10000], [-10000, 10000, 9999], [None, 10000, 10000, 10000], None),
    (3, [2, 2, 1, 1], [2, 1, 3, 3, 3], None, None),
    (5, [], [], [None], None),
    (1, big_nums, big_adds, None, 2.0),
    (5000, big_nums, big_adds, None, 2.0),
    (10001, big_nums, big_adds[:1] + [0] * 0, None, 2.0),
]

# Fix case 5: k=2, empty nums, first add would violate guarantee; use valid sequence instead
cases[4] = (2, [3], [7, 7, 1], [None, 3, 7, 7], None)

passed = 0
total = len(cases)
for i, (k, nums, adds, expected, limit) in enumerate(cases, 1):
    if expected is None:
        expected = brute(k, nums, adds)
    try:
        start = time.time()
        got = run(k, nums, adds)
        elapsed = time.time() - start
        if got != expected:
            inp = f"k={k}, nums={nums if len(nums) <= 20 else f'<{len(nums)} items>'}, adds={adds if len(adds) <= 20 else f'<{len(adds)} items>'}"
            exp_s = expected if len(expected) <= 20 else f"<{len(expected)} items>"
            got_s = got if len(got) <= 20 else f"<{len(got)} items, first mismatch at {next((j for j, (a, b) in enumerate(zip(got, expected)) if a != b), min(len(got), len(expected)))}>"
            print(f"FAIL case {i}: input={inp}, expected={exp_s}, got={got_s}")
        elif limit is not None and elapsed > limit:
            print(f"FAIL case {i}: input=k={k}, <large input>, expected=finish within {limit}s, got={elapsed:.2f}s")
        else:
            print(f"PASS case {i}")
            passed += 1
    except Exception as e:
        inp = f"k={k}, nums={nums if len(nums) <= 20 else f'<{len(nums)} items>'}, adds={adds if len(adds) <= 20 else f'<{len(adds)} items>'}"
        print(f"FAIL case {i}: input={inp}, expected={expected if len(expected) <= 20 else '<large>'}, got={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)