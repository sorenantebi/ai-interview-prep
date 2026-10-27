import sys
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


def reference(temperatures):
    res = [0] * len(temperatures)
    stack = []
    for i, t in enumerate(temperatures):
        while stack and t > temperatures[stack[-1]]:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]

rng = random.Random(12345)
N = 10 ** 5

random_large = [rng.randint(30, 100) for _ in range(N)]
random_small = [rng.randint(30, 35) for _ in range(200)]
zigzag = [30 if i % 2 == 0 else 100 for i in range(1000)]

cases = [
    ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),   # example 1
    ([30, 40, 50, 60], [1, 1, 1, 0]),                                # example 2
    ([30, 60, 90], [1, 1, 0]),                                       # example 3
    ([50], [0]),                                                     # single element
    ([70, 70, 70, 70], [0, 0, 0, 0]),                                # all equal (strictly warmer)
    ([100, 90, 80, 70, 60, 50, 30], [0] * 7),                        # strictly decreasing
    ([30, 30, 31, 30, 31], [2, 1, 0, 1, 0]),                         # duplicates
    ([30, 100], [1, 0]),                                             # two elements, min/max bounds
    ([100, 30], [0, 0]),                                             # two elements, descending
    (zigzag, reference(zigzag)),                                     # alternating
    (random_small, reference(random_small)),                         # random small range, many duplicates
    (list(range(30, 71)) * 1, reference(list(range(30, 71)))),       # increasing run
    ([30] * (N - 1) + [31], [N - 1 - i for i in range(N - 1)] + [0]),  # large: warm day at the end
    ([100 - (i * 70 // N) for i in range(N)], [0] * N),              # large: non-increasing
    (random_large, reference(random_large)),                         # large random
]

passed = 0
total = len(cases)

for idx, (temps, expected) in enumerate(cases, 1):
    short = temps if len(temps) <= 20 else f"<list of length {len(temps)}>"
    short_exp = expected if len(expected) <= 20 else f"<list of length {len(expected)}>"
    try:
        start = time.time()
        got = Solution().dailyTemperatures(list(temps))
        elapsed = time.time() - start
        got_list = list(got) if got is not None else got
        if got_list == expected:
            passed += 1
            print(f"PASS case {idx}")
        else:
            shown = got_list if got_list is None or len(got_list) <= 20 else f"<list of length {len(got_list)}>"
            print(f"FAIL case {idx}: input={short}, expected={short_exp}, got={shown}")
    except Exception as e:
        print(f"FAIL case {idx}: input={short}, expected={short_exp}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)